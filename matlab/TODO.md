# MATLAB Proxy auf Azure Databricks

**Umgebung:** Azure Databricks, MATLAB R2025b, Databricks Runtime 16.4-LTS

---

## 1. Zielsetzung

Integration von **MATLAB Proxy** auf einer **Azure Databricks Clusterumgebung**, um MATLAB über den Webbrowser (via `driver-proxy`) innerhalb einer sicheren VNet-Infrastruktur auszuführen.

---

## 2. Aktueller Zustand

### 2.1 Architekturüberblick

* **Databricks Cluster:**
  Name: `MATLAB-on-Databricks`
  Status: *Running / Pending / Terminated*
  Typ: *Standard Cluster (Driver + Worker)*

* **MATLAB Installation:**

  * Bereitgestellt über einen benutzerdefinierten Docker-Container (MATLAB + matlab-proxy).
  * Zugriff auf MATLAB Proxy über URL:

    ```sh
    https://adb-2761604089493481.1.azuredatabricks.net/driver-proxy/o/2761604089493481/1007-175019-rgpgf1wc/3000/matlab
    ```

* **Init Script:**
  `/Volumes/matlab-on-databricks/default/myvolume/00-matlab-proxy-init.sh`
  Wird beim Clusterstart ausgeführt und startet den MATLAB Proxy (`matlab-proxy-app`).

---

## 3. Aktuelle Symptome und Beobachtungen

| Symptom                                                  | Beschreibung                                                                                               |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `502 Bad Gateway` beim Zugriff auf Proxy-URL             | Der Nginx-Proxy von Databricks kann die Proxy-App nicht erreichen oder diese hängt in der Lizenzprüfung.   |
| MATLAB UI zeigt *“Starting... may take several minutes”* | MATLAB Proxy wird gestartet, kann sich aber nicht erfolgreich bei den MathWorks-Diensten authentifizieren. |
| Automatisches *Sign-Out* nach Timeout                    | Lizenz-Authentifizierung schlägt fehl.                                                                     |
| `mlc.services.mathworks.com` nicht erreichbar            | DNS-Fehler → keine Internetauflösung.                                                                      |
| `curl: (6) Could not resolve host`                       | VNet hat keine aktive DNS-Weiterleitung oder Internetzugang.                                               |

---

## 4. Root Cause (Hauptursache)

### 4.1 Netzwerkebene

* **VNet Peering** ist **deaktiviert** → Databricks Managed VNet kann nicht mit dem kundenseitigen Hub-VNet kommunizieren.
* Ohne aktives Peering ist kein **DNS-Forwarding** und keine **Internet-Egress-Verbindung** vorhanden.
* Die Domains der MathWorks-Lizenzserver (`*.mathworks.com`) sind dadurch **nicht erreichbar**.

### 4.2 Lizenzierungsebene

* MATLAB Proxy nutzt **Online Licensing** (MathWorks Login).
  Dafür sind folgende Endpunkte notwendig:

  ```
  login.mathworks.com
  mlc.services.mathworks.com
  licensing.mathworks.com
  services.mathworks.com
  www.mathworks.com
  ```
* Ohne Zugriff auf diese Endpunkte schlägt die Lizenzprüfung fehl.

---

## 5. Technische Beweise

### 5.1 Cluster-Log-Auszug

```
INFO: Starting matlab-proxy-app on 0.0.0.0:8888/matlab
INFO: Waiting for matlab-proxy-app to start
INFO: matlab-proxy-app is healthy at http://127.0.0.1:8888/matlab
INFO: MATLAB Proxy URL written to /databricks/driver/matlab-proxy/matlab-url.txt
```

### 5.2 Netzwerk-Test

```bash
%sh
for h in login.mathworks.com mlc.services.mathworks.com licensing.mathworks.com services.mathworks.com www.mathworks.com; do
  echo CHECK $h; curl -sSfI https://$h | head -n1 || echo "FAIL $h"
done
```

**Ergebnis:**

```
CHECK login.mathworks.com     → HTTP/2 302
CHECK mlc.services.mathworks.com → FAIL (DNS)
CHECK licensing.mathworks.com   → HTTP/1.1 404
CHECK services.mathworks.com    → HTTP/2 500
CHECK www.mathworks.com         → HTTP/2 200
```

Interpretation:

* Lizenzserver `mlc.services.mathworks.com` nicht auflösbar → **DNS/Peering-Problem**.
* Andere Domains teilweise erreichbar → **teilweise Egress vorhanden**, aber kein vollständiger Zugriff.

---

## 6. Maßnahmen & Lösungen

### 6.1 Netzwerkkonfiguration

1. **VNet Peering reaktivieren**

   * Azure Portal → *Databricks Workspace → Networking → Virtual Network Peerings*
   * Klick: **Add Peering**
   * Optionen:

     * Allow Virtual Network Access ✅
     * Allow Forwarded Traffic ✅
   * Sicherstellen, dass **beide Richtungen** aktiv sind (Databricks ↔ Hub).

2. **DNS- und Egress-Freigabe**

   * In NSG / Firewall / Azure Firewall FQDN-Regel erstellen:

     ```
     *.mathworks.com
     Port: 443
     Protocol: HTTPS
     Action: Allow
     ```
   * Wenn PrivateLink aktiv ist → Outbound Proxy oder NAT Gateway konfigurieren.

3. **Test nach Reaktivierung**

   ```bash
   %sh
   sudo apt-get update && sudo apt-get install -y dnsutils
   nslookup mlc.services.mathworks.com
   curl -sSfI https://mlc.services.mathworks.com | head -n1
   ```

   Erwartet:

   ```
   Name: mlc.services.mathworks.com
   Address: <valid IP>
   HTTP/2 200
   ```

---

### 6.2 Alternative: Offline Licensing (NLM)

Falls kein Internetzugriff erlaubt ist:

```bash
export MLM_LICENSE_FILE=27000@<license-server-host>
```

* Lizenzserver muss im Cluster erreichbar sein (über internes Netzwerk).
* Dadurch entfällt Online-Authentifizierung.

---

### 6.3 Init Script – Optimierte Version

```bash
#!/bin/bash
set -euxo pipefail

echo "=== MATLAB Proxy Init Script Starting ==="

export HOME=/databricks/driver
mkdir -p ${HOME}/matlab-proxy/logs

export MWI_BASE_URL="/matlab"
export MWI_APP_PORT=8888
export MWI_ENABLE_TOKEN_AUTH=false
export MWI_USE_COOKIE_CACHE=true

nohup matlab-proxy-app > ${HOME}/matlab-proxy/logs/proxy.log 2>&1 &

sleep 10
if pgrep -f "matlab-proxy-app" > /dev/null; then
    echo "SUCCESS: MATLAB Proxy started."
else
    echo "ERROR: MATLAB Proxy failed to start." >&2
    exit 1
fi

echo "=== MATLAB Proxy Init Script Completed ==="
```

Upload-Pfad:

```
/Volumes/matlab-on-databricks/default/myvolume/00-matlab-proxy-init.sh
```

---

## 7. To-Do-Liste

| Status | Aufgabe                                | Beschreibung                                                          |
| ------ | -------------------------------------- | --------------------------------------------------------------------- |
| ☐      | **VNet Peering prüfen und aktivieren** | Peering zwischen Databricks VNet und Hub-VNet herstellen (beidseitig) |
| ☐      | **DNS-Auflösung testen**               | `nslookup mlc.services.mathworks.com` muss IP zurückgeben             |
| ☐      | **Outbound-Firewall prüfen**           | HTTPS-Zugriff auf `*.mathworks.com` erlauben                          |
| ☐      | **Cluster neu starten**                | Nach Netzwerkänderungen                                               |
| ☐      | **MATLAB Proxy erneut starten**        | Über Init-Skript oder GUI                                             |
| ☐      | **Lizenzen testen (Online/NLM)**       | Prüfen, ob MATLAB GUI nach Login startet                              |
| ☐      | **Web Terminal aktivieren (optional)** | Für manuelle Debug-Sessions im Cluster                                |
| ☐      | **Logging erweitern**                  | `/databricks/driver/matlab-proxy/logs/proxy.log` sammeln              |

---

Der MATLAB Proxy startet korrekt, jedoch blockieren **DNS-Auflösung und Internetzugriff** aufgrund eines **deaktivierten VNet-Peerings** die Lizenzprüfung.
Nach Aktivierung des Peerings und Freigabe der MathWorks-Domains wird MATLAB ordnungsgemäß starten und die Browser-UI nutzbar sein.


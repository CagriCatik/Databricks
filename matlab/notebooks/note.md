Below are the **example notebook files** that align with your MATLAB-on-Databricks setup.
They demonstrate how to start the MATLAB Proxy and interact with Databricks data.

---

### **1. `matlab_proxy_demo.ipynb`**

Purpose: Start and verify MATLAB Proxy from a Databricks notebook.

```python
# Databricks notebook source
# MAGIC %md
# MAGIC ## MATLAB Proxy Startup Demo
# MAGIC This notebook validates that the MATLAB Proxy service is running
# MAGIC and accessible on the Databricks driver node.

# COMMAND ----------

# MAGIC %sh
# MAGIC echo "Checking MATLAB Proxy process..."
# MAGIC ps -ef | grep matlab-proxy-app | grep -v grep || echo "Proxy not running."

# COMMAND ----------

# MAGIC %sh
# MAGIC echo "Verifying port 3000..."
# MAGIC ss -ltnp | grep 3000 || echo "Port 3000 not found."

# COMMAND ----------

# MAGIC %sh
# MAGIC echo "Checking MATLAB URL file..."
# MAGIC cat /databricks/driver/matlab-proxy/matlab-url.txt || echo "URL not found."

# COMMAND ----------

# MAGIC %python
import requests, os, time

url_file = "/databricks/driver/matlab-proxy/matlab-url.txt"
if not os.path.exists(url_file):
    raise FileNotFoundError("MATLAB URL file not found. Init script may have failed.")

with open(url_file) as f:
    matlab_url = f.read().strip()

print("MATLAB Proxy URL:", matlab_url)
print("Verifying connection...")

for i in range(10):
    try:
        r = requests.get(matlab_url, timeout=10)
        if r.status_code in (200, 302):
            print("MATLAB Proxy reachable at:", matlab_url)
            break
    except Exception as e:
        print(f"Attempt {i+1}: still waiting...")
        time.sleep(5)
else:
    raise RuntimeError("MATLAB Proxy not reachable after retries.")

# COMMAND ----------

# MAGIC %md
# MAGIC **Expected Output**
# MAGIC
# MAGIC - MATLAB Proxy process visible in `ps -ef`
# MAGIC - Port `3000` open
# MAGIC - URL file exists at `/databricks/driver/matlab-proxy/matlab-url.txt`
# MAGIC - HTTP 200/302 response from the proxy endpoint
```

---

### **2. `databricks_connection_example.mlx`**

Purpose: Run MATLAB commands inside Databricks and access data via JDBC.

```matlab
%% Databricks Connectivity Example
% This example demonstrates how to connect MATLAB to Databricks data sources.

% Define Databricks parameters
DATABRICKS_HOST = "https://adb-2761604089493481.1.azuredatabricks.net";
TOKEN = "dapiXXXXXXXXXXXXXXXXXXXXXXXX";
HTTP_PATH = "/sql/1.0/warehouses/abc123xyz456";
DATABASE = "default";

%% Connect via JDBC
% Requires Database Toolbox
conn = databricksJDBC(DATABRICKS_HOST, TOKEN, HTTP_PATH);

%% Query a Delta Table
sqlquery = "SELECT * FROM samples.nyctaxi LIMIT 10";
data = fetch(conn, sqlquery);
disp(data);

%% Close Connection
close(conn);

%% Verify MATLAB Information
ver
matlabroot
license
```

---

### **Optional Helper Notebook: `matlab_diagnostics.ipynb`**

Purpose: Run diagnostics if MATLAB Proxy fails.

```python
# COMMAND ----------
# MAGIC %md
# MAGIC ## MATLAB Diagnostics Notebook

# COMMAND ----------
# MAGIC %sh
echo "=== DNS Check ==="
for h in login.mathworks.com mlc.services.mathworks.com licensing.mathworks.com services.mathworks.com www.mathworks.com; do
  echo "CHECK $h"
  nslookup $h 2>/dev/null || echo "FAIL $h"
done

echo "=== Proxy Check ==="
curl -sI http://127.0.0.1:3000/matlab | head -n 1 || echo "Proxy unreachable."

# COMMAND ----------
# MAGIC %python
import os
log_path = "/databricks/driver/matlab-proxy/matlab-proxy.out"
if os.path.exists(log_path):
    with open(log_path) as f:
        print(f.read()[-2000:])
else:
    print("MATLAB Proxy log not found.")
```

---

### Notes

* Place notebooks under:

  ```
  /notebooks/
  ├── matlab_proxy_demo.ipynb
  ├── databricks_connection_example.mlx
  └── matlab_diagnostics.ipynb
  ```

* These notebooks **do not require GUI access**; they run within the Databricks workspace.

* After successful proxy verification, MATLAB is accessible via the URL written by the init script.

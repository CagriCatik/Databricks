# MATLAB on Databricks

> [!IMPORTANT]
> **Why This Project**

* Run MATLAB directly on **Azure Databricks** through a **browser-based interface**.
* Eliminate RDP or X11 forwarding; access MATLAB securely and seamlessly online.
* Use MATLAB’s familiar environment and toolboxes inside a unified, scalable Databricks workspace.
* Execute computations **where the data resides**, reducing latency and data movement.
* Maintain data security and compliance by **keeping data within the lakehouse** (Delta tables, object storage).
* Ensure consistent, reproducible environments using **Databricks cluster init scripts or Docker images**.
* Leverage Databricks autoscaling to run large MATLAB workloads efficiently across multiple nodes.

---

## Overview

This repository provides a **ready-to-use framework** for integrating **MATLAB** within **Azure Databricks**.
It enables running MATLAB interactively inside a Databricks environment using [`matlab-proxy`](https://github.com/mathworks/matlab-proxy), with no desktop setup required.

---

### Key Capabilities

* **MATLAB Proxy Integration**
  Launch a full MATLAB desktop session in the browser. The session runs inside a Databricks cluster or container, removing the need for RDP or manual installations.

* **Databricks Connectivity**
  Connect MATLAB to Databricks clusters, SQL Warehouses, and data stores using:

  * Personal Access Tokens (PATs)
  * JDBC/ODBC connections
  * [MATLAB Interface for Databricks](https://www.mathworks.com/solutions/partners/databricks.html)

* **Data In-Place Execution**
  Run MATLAB code directly on Delta tables without data export or duplication.

* **Cluster-Scale Computation**
  Utilize Databricks’ distributed compute for simulation, parallel computing, and model evaluation.

* **Unified Notebook Workflow**
  Combine MATLAB with Python, SQL, and Spark in collaborative Databricks notebooks.

---

## Features

| Feature                     | Description                                                                       |
| --------------------------- | --------------------------------------------------------------------------------- |
| **Browser-based MATLAB UI** | Access a full MATLAB session via the web browser, powered by Databricks compute.  |
| **No Desktop Dependency**   | Runs fully inside Databricks—no RDP or local installation required.               |
| **Secure and Auditable**    | Uses Databricks authentication and workspace controls; execution is fully logged. |
| **Cluster Automation**      | Reproducible setup through init scripts and Docker images.                        |
| **Interoperability**        | Integrate MATLAB analytics with Python, SQL, and Spark workflows.                 |
| **Scalability**             | Leverage autoscaling clusters for parallel MATLAB workloads.                      |

---

## Architecture Overview

The integration is composed of three main components:

1. **Container Image (Dockerfile)**

   * Base: `databricksruntime/standard:16.4-LTS`
   * Includes MATLAB R2025b with selected toolboxes.
   * Installs and configures `matlab-proxy`.
   * Exposes MATLAB on port **3000** for Databricks driver-proxy routing.
   * Supports both **Online Licensing** and **Network License Manager (NLM)** modes.

2. **Cluster Init Script**

   * Automatically starts `matlab-proxy-app` on the Databricks driver node.
   * Writes the accessible MATLAB URL to:
     `/databricks/driver/matlab-proxy/matlab-url.txt`
   * Performs startup health checks and optional warm-up for faster loading.
   * Works with Databricks Volumes or DBFS.

3. **Networking and Licensing**

   * Requires outbound HTTPS access to MathWorks services or internal NLM access.
   * Verified domains:

     ```
     login.mathworks.com
     mlc.services.mathworks.com
     licensing.mathworks.com
     services.mathworks.com
     www.mathworks.com
     ```
   * Alternative: use NLM via `MLM_LICENSE_FILE=27000@<license-server-host>` if internet egress is blocked.

---

## Deployment Steps

### 1. Build and Push the Container

Build the MATLAB-enabled Docker image and push it to your container registry (ACR, ECR, or Docker Hub).
Example:

```
docker build -t <registry>/matlab-on-databricks:R2025b-16.4 .
docker push <registry>/matlab-on-databricks:R2025b-16.4
```

### 2. Create or Configure the Databricks Cluster

* Select a **custom container** cluster configuration.
* Use the pushed Docker image as the base container.
* Ensure cluster networking allows outbound HTTPS to MathWorks.

### 3. Attach the Init Script

* Store the script at one of:

  * `/Volumes/matlab-on-databricks/default/myvolume/00-matlab-proxy-init.sh`
  * `dbfs:/databricks/init/00-matlab-proxy-init.sh`
* Attach the script under *Cluster → Advanced Options → Init Scripts*.

### 4. Start Cluster and Verify MATLAB Proxy

* Check log output in `/databricks/driver/matlab-proxy/matlab-proxy.out`.
* The MATLAB Proxy URL will be written to:
  `/databricks/driver/matlab-proxy/matlab-url.txt`.

### 5. Open MATLAB in Browser

Access MATLAB via the Databricks driver-proxy URL pattern:

```
https://<databricks-instance>/driver-proxy/o/<org-id>/<cluster-id>/3000/matlab
```

Example:

```
https://adb-2761604089493481.1.azuredatabricks.net/driver-proxy/o/2761604089493481/1007-175019-rgpgf1wc/3000/matlab
```

Sign in using your MathWorks Account or an internal NLM license.

---

## Networking and Security Configuration

* Confirm **VNet Peering** between Databricks and your hub network is active.
* If egress is controlled by Azure Firewall or NAT, allow the domains listed above.
* For **PrivateLink** setups, configure explicit outbound routes to MathWorks or use an NLM.
* Optional: configure corporate proxy via `HTTPS_PROXY` and `NO_PROXY` environment variables in the init script.

---

## Repository Structure

```
matlab-on-databricks/
├── cluster/
│   ├── init/
│   │   ├── 00-matlab-proxy-init.sh        # Cluster init script for proxy startup
│   │   └── configure_matlab_runtime.sh    # Optional runtime configuration
├── docker/
│   └── Dockerfile                         # MATLAB container image definition
├── notebooks/
│   ├── matlab_proxy_demo.ipynb            # Demonstration notebook
│   └── databricks_connection_example.mlx  # MATLAB connectivity example
├── docs/
│   └── assets/
│       ├── matlab_logo.png
│       └── databricks_logo.png
└── README.md
```

---

## Troubleshooting Guide

| Issue                         | Cause                                        | Resolution                                                          |
| ----------------------------- | -------------------------------------------- | ------------------------------------------------------------------- |
| **502 Bad Gateway**           | Proxy not running or port mismatch           | Verify init script uses port `3000` and container exposes the same. |
| **MATLAB login timeout**      | Licensing server unreachable                 | Check VNet and outbound access to `*.mathworks.com`.                |
| **Automatic sign-out**        | Session not validated due to DNS/SSL failure | Enable DNS resolution via active peering and NAT.                   |
| **No file at matlab-url.txt** | Init script failed early                     | Check `/databricks/driver/matlab-proxy/matlab-proxy.out`.           |
| **Proxy starts but UI slow**  | Cold start of MATLAB backend                 | Keep warm-up enabled in init script.                                |

---

## References

* [MATLAB Proxy on GitHub](https://github.com/mathworks/matlab-proxy)
* [MATLAB Interface for Databricks](https://www.mathworks.com/solutions/partners/databricks.html)
* [Databricks Documentation](https://docs.databricks.com/)
* [Azure Databricks Security](https://learn.microsoft.com/en-us/azure/databricks/)
* [MathWorks Licensing Guide](https://www.mathworks.com/help/matlab/matlab_env/install-products.html)
* [Installation](https://de.mathworks.com/content/dam/mathworks/mathworks-dot-com/products/reference-architectures/matlab-databricks-v5-3-1-win64.zip)

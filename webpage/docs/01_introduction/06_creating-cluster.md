# Creating a Cluster in Databricks

This guide explains how to create and manage a Databricks cluster, the foundational compute engine for executing Apache Spark jobs within the platform. Proper cluster configuration is critical for performance, cost management, and eligibility for the **Databricks Data Engineer Associate** certification.

---

## What Is a Databricks Cluster?

A **cluster** is a set of virtual machines (VMs) coordinated to run Spark applications in parallel. It consists of:

- **Driver Node**: Maintains the SparkContext, coordinates tasks, and manages execution.
- **Worker Nodes**: Perform distributed data processing as instructed by the driver.

Clusters power all notebooks, jobs, and streaming applications in Databricks.

---

## Accessing Cluster Management

To create or manage clusters:

1. Open the **Databricks UI**.
2. Click the **Compute** tab in the **left sidebar**.

This opens the cluster management interface.

---

## Creating a Cluster: Step-by-Step Instructions

### 1. Start Cluster Creation

- Under **All-Purpose Compute**, click **Create Compute**.
- Enter a name for the cluster (e.g., `Demo Cluster`).

### 2. Cluster Policy

- Set **Cluster Policy** to `Unrestricted`.
  - Allows full customization.
  - May be restricted in enterprise environments.

---

## Cluster Configuration Options

### Cluster Mode

- **Single Node**:
  - Driver performs all computation.
  - Suitable for testing or small data volumes.
- **Multi-Node**:
  - One driver and multiple workers.
  - Recommended for production or high-volume workloads.

### Access Mode

- **Single User**:
  - Private to creator.
  - Supports all languages (SQL, Python, Scala, etc.).
- **Shared**:
  - Accessible to multiple users.
  - Supports SQL and Python only.

---

## Runtime Environment

### Databricks Runtime

- Pre-packaged Spark, Scala, Python, and ML libraries.
- For course or certification:
```

Databricks Runtime 13.3 LTS

```

> **Note**: Runtime version affects feature compatibility. Match it to course or workload requirements.

---

## Photon Engine

- **Photon**: Vectorized query engine built in C++.
- Enhances performance for SQL-heavy workloads.
- Toggle **Photon Acceleration** ON if available.

---

## Node Configuration

### VM Type Selection

- Choose VM types based on:
- Memory
- Cores
- Disk
- VM availability varies by cloud provider (AWS, Azure, GCP).

> **Guidance**: Use default VMs for learning. Match specs to workloads in production.

### Worker Configuration

- **Fixed Workers**: Set a specific number (e.g., 3).
- **Autoscaling**: Set a min/max range (e.g., 2–5).
- Scales up or down based on job demands.

### Driver Configuration

- Driver instance type may match or differ from worker nodes.

---

## Cluster Lifecycle Settings

### Auto Termination

- Automatically shuts down idle clusters.
- Prevents unnecessary billing.
- Recommended setting: `30 minutes` of inactivity.

### DBU Consumption

- **DBU (Databricks Unit)**: Billing unit based on runtime, instance type, and usage time.
- Fewer nodes or simpler runtimes consume fewer DBUs.

---

## Launching the Cluster

- Review the configuration summary on the right panel.
- Click **Create**.

Databricks provisions VMs, configures the environment, and starts the cluster.

---

## Managing a Cluster

After the cluster is created:

- Go to **Compute** to manage it.
- Monitor status: `Running`, `Terminating`, `Terminated`.

### Actions Available

- **Start / Terminate**
- **Edit** configuration (restart required)
- **Delete**
- **Manage Permissions**

### Monitoring Features

- **Event Log**: Tracks cluster lifecycle events.
- **Driver Logs**: Capture Spark job execution details.

---

## Community Edition Limitations

Users of **Databricks Community Edition** are restricted to a single preconfigured cluster:

| Feature                | Availability              |
|------------------------|---------------------------|
| Cluster Type           | Single-node only          |
| CPU/RAM                | 2 cores, 15 GB RAM         |
| VM Configuration       | Not configurable          |
| Photon Support         | Not available             |
| Autoscaling            | Not available             |
| Runtime Selection      | Limited, but supported    |

---

## Terminating a Cluster

To shut down an active cluster:

1. Navigate to the **Compute** page.
2. Click on the target cluster.
3. Select **Terminate**.

This stops billing and releases all associated compute resources.

---

## Summary

| Feature                     | Full Databricks | Community Edition |
|-----------------------------|-----------------|-------------------|
| Multi-node support          | ✅ Yes           | ❌ No              |
| Custom VM selection         | ✅ Yes           | ❌ No              |
| Autoscaling                 | ✅ Yes           | ❌ No              |
| Access modes (Single/Shared)| ✅ Yes           | ❌ No              |
| Photon engine               | ✅ Yes           | ❌ No              |
| Runtime selection           | ✅ Yes           | ✅ Yes             |
| Event and driver logs       | ✅ Yes           | ✅ Partial         |

Understanding and managing clusters is a critical skill for both certification preparation and production deployment within the Databricks Lakehouse Platform.
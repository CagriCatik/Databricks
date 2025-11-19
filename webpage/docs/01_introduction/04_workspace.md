# Databricks Workspace Overview

## Workspace Homepage

The Workspace homepage offers streamlined onboarding with tiles such as **Get started**, **Recents**, and **Popular**. These provide shortcuts to common actions like notebook creation, file uploads, query editing, and viewing frequently used assets. Displayed content varies based on workspace entitlements. ([Microsoft Learn][1])

---

## Sidebar Navigation and New‑Menu

The collapsible sidebar leads to core platform sections: **Workspace**, **Recents**, **Catalog**, **Jobs & Pipelines**, **Compute**, **Marketplace**, and persona-based tabs (SQL, Data Engineering, Machine Learning). Features requiring additional entitlements are marked with a lock icon. ([Microsoft Learn][1])
The **+ New** menu enables creation of workspace objects (notebooks, jobs, dashboards, alerts, repos) and compute resources. ([Microsoft Learn][1])

---

## Workspace Browser and Object Management

The unified browser supports nested folder structures and drag‑and‑drop placement of notebooks, libraries, experiments, dashboards, files, and alerts. Git folders are integrated alongside workspace folders. You can manage permissions, share folders, and reposition objects using context menus. Full filenames (including extensions) must be unique within a folder. ([docs.databricks.com][2])

---

## Recents and Popular Sections

* **Recents** displays your accessed objects across workloads: notebooks, queries, dashboards, experiments, alerts, and Unity Catalog resources.
* **Popular** highlights organization-wide high-interaction assets over the past 30 days. ([Microsoft Learn][1])

---

## Catalog Tab (Unity Catalog Integration)

The **Catalog** UI enables governance and discovery of data assets across workspaces:

* It lists catalogs, schemas (formerly databases), tables, views, ML models, and volumes.
* Supports centralized access policies and lineage tracking. ([docs.databricks.com][3], [campus.datacamp.com][4])

---

## Jobs & Pipelines (Workflows) Tab

Under this tab, you manage job orchestration and pipelines:

* Create scheduled jobs and Lakeflow pipelines.
* Define task dependencies, manage retries, and monitor job execution logs. ([Microsoft Learn][1], [Microsoft Learn][5])

---

## Compute Tab

Manages compute infrastructure:

* All-purpose clusters for interactive work.
* Job clusters for pipeline execution.
* SQL warehouses for query workloads.
  Capable of applying fine-grained cluster policies, autoscaling options, and retention limits. Users can pin clusters to preserve configurations beyond 30 days. ([campus.datacamp.com][4], [Microsoft Learn][1])

---

## SQL, Data Engineering, Machine Learning Tabs

* **SQL**: SQL editor interface, dashboards, alerting, and query history.
* **Data Engineering**: Monitoring Data Ingestion flows, job runs, pipeline diagnostics.
* **Machine Learning**: MLflow experiments, feature store, model registry—excluded from Data Engineer Associate exam scope. ([Microsoft Learn][1], [Microsoft Learn][5])

---

## Top Bar Controls

* **Search**: Unified search across all workspace objects including notebooks, tables, dashboards, jobs, files, repos, alerts, and experiments. Filters improve discoverability. ([Microsoft Learn][1])
* **Workspace Switcher**: Switch between multiple workspace environments within the same account. ([Microsoft Learn][1], [docs.databricks.com][6])
* **User Settings**: Access **Settings** menu for user preferences, token management, admin configurations, and language change options. ([Microsoft Learn][1], [docs.databricks.com][7])
* **Databricks Assistant**: Integrated AI assistant offers code generation, query optimization, and documentation suggestions. Verification with documentation is advised. ([docs.databricks.com][8], [Microsoft Learn][1])

---

## Workspace-Level Controls & Security

Admins manage workspace behavior via **Settings**, including:

* Storage policies, UI toggles, notebook result storage, third-party integrations, admin permissions, and sensitive feature enablement (e.g., terminal, preview features). ([docs.databricks.com][7])
* Workspaces now support binding of storage or service credentials and external locations to specific workspaces for isolation use cases. ([docs.databricks.com][9])

---

## Databricks Apps

Workspaces support building full-stack interactive **Databricks Apps** that integrate Delta Lake, ML models, notebooks, and Unity Catalog assets. These run on managed infrastructure and can be shared within the workspace. ([docs.databricks.com][10])

---

## Workspaces at Account Level

A Databricks deployment is organized into an **account** containing one or more workspaces. Unity Catalog integration enables unified identity and governance across workspaces. Best practice for enterprises includes isolating dev, staging, production, or sensitive-data environments into separate workspaces while tracking governance centrally. ([docs.databricks.com][3])

---

## Best Practice Tips

* Use separate environments (Dev / Prod / Staging) to reduce data risk and optimize governance.
* Employ Git folders and Repos to coordinate versioned collaboration.
* Use folder-level ACLs to manage permissions.
* Keep UX clean by separating sandbox vs production assets.
* Isolate storage and credentials per workspace when sensitive data is involved. ([ittechgenie.com][11])

---

## Certification Alignment – Data Engineer Associate

Relevant areas for study:

* **Workspace browser and folder structure**
* **Cluster creation and policy management (Compute)**
* **Job orchestration and pipelines (Jobs & Pipelines)**
* **SQL querying and dashboard management**
  Familiarity with search, object organization, and entitlement-aware UI behavior is essential.

---

## Summary Table

| Area                 | Key Focus                                                           |
| -------------------- | ------------------------------------------------------------------- |
| Workspace Browser    | Manage notebooks, folders, Git repos, permissions                   |
| Sidebar & Navigation | Workspace, Recents, Catalog, Jobs & Pipelines, Compute, Marketplace |
| Top Bar              | Search, workspace switching, settings, AI Assistant                 |
| Catalog              | Unity Catalog governance of data assets and models                  |
| Compute Tab          | Cluster/warehouse creation, policy enforcement, autoscaling         |
| Jobs & Pipelines     | Pipeline orchestration, job scheduling, failure retries, monitoring |
| Databricks Apps      | Built-in app creation & integration                                 |
| Workspace Security   | Credentials binding, settings, admin control, content isolation     |

---

[Databricks Workspace Interface Tour](https://www.youtube.com/watch?v=nU6jD74lzak)

[1]: https://learn.microsoft.com/en-us/azure/databricks/workspace/navigate-workspace "Navigate the workspace UI - Azure Databricks | Microsoft Learn"
[2]: https://docs.databricks.com/aws/en/workspace/workspace-browser/ "Workspace browser | Databricks Documentation"
[3]: https://docs.databricks.com/aws/en/getting-started/concepts "Databricks components | Databricks Documentation"
[4]: https://campus.datacamp.com/courses/introduction-to-databricks/introduction-to-databricks-1?ex=3 "Overview of the Databricks UI - DataCamp"
[5]: https://learn.microsoft.com/en-us/azure/databricks/workspace/workspace-assets "Introduction to workspace objects - Azure Databricks"
[6]: https://docs.databricks.com/aws/en/admin/workspace/ "Create a workspace | Databricks Documentation"
[7]: https://docs.databricks.com/aws/en/admin/workspace-settings/ "Manage your workspace | Databricks Documentation"
[8]: https://docs.databricks.com/gcp/en/workspace/ "Workspace UI | Databricks Documentation"
[9]: https://docs.databricks.com/aws/en/release-notes/product/2025/march "March 2025 | Databricks Documentation"
[10]: https://docs.databricks.com/aws/en/release-notes/product/2025/may "May 2025 | Databricks Documentation"
[11]: https://ittechgenie.com/DataBricks/IntroductionToDataBricks "Introduction to DataBricks ItTechGenie"

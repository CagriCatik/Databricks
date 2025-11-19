# Importing Course Materials into Databricks

This guide describes two methods for importing course notebooks into your Databricks workspace:

- **Git Folder Cloning**: For full-featured cloud-based Databricks environments (trial or enterprise)
- **DBC Archive Import**: For Databricks Community Edition users

Each method enables access to course materials for hands-on execution and learning.

---

## Method 1: Git Folder Import (Full Databricks Environments)

Databricks supports native integration with Git version control systems (e.g., GitHub, GitLab, Bitbucket) using **Git folders**. This is the recommended method for users on AWS, Azure, or GCP-based workspaces.

### Step-by-Step: Clone a GitHub Repository

#### 1. Copy Repository URL

- Navigate to the course's GitHub repository
- Copy the full URL: [https://github.com/your-org/course-repo.git](https://github.com/your-org/course-repo.git)

#### 2. Open Workspace Tab

- In the left sidebar, click **Workspace**

#### 3. Create Git Folder

- Click the **Create** button in the top-right
- Select **Git Folder**

#### 4. Paste Repository URL

- Paste the copied URL into the **Git repository URL** field
- Databricks auto-detects provider and assigns a default folder name

#### 5. Confirm Cloning

- Click **Create Git Folder**

The Git folder is now visible in the workspace. All repository notebooks are accessible for use or editing.

### Git Folder Benefits

- Integrated Git version control
- Push/pull changes directly from Databricks UI
- Continuous sync with remote branches
- Ideal for CI/CD workflows and collaboration

---

## Verifying Imported Notebooks

To confirm import success:

1. Open the **Workspace** tab
2. Expand your **Home** directory
3. You should see:

- The previously created `Demo` folder (if applicable)
- A new Git folder with the imported course repository

Course notebooks are now available and ready for execution.

---

## Method 2: Import DBC Archive (Community Edition Compatible)

The Databricks Community Edition does not support Git folder integration. Instead, use the **DBC file** import method. A `.dbc` file is a bundled export of one or more Databricks notebooks.

### Step-by-Step: Import DBC File

#### 1. Download Archive File

- Navigate to the **Resources** section of the course
- Download the `.dbc` file provided with the learning material

#### 2. Open Workspace Tab

- In the Community Edition UI, go to **Workspace**

#### 3. Use Import Option

- Click the **three-dot menu** (`⋮`) next to the `Home` or target folder
- Select **Import**

#### 4. Upload Archive

- In the import dialog:
- Click **Browse**
- Select the `.dbc` file from your device

#### 5. Complete Import

- Click **Import**
- The course notebooks will appear in the selected folder

> **Note**: DBC files preserve the original folder structure and notebook content.

---

## Summary of Import Methods

| Feature                  | Full Databricks | Community Edition |
|--------------------------|-----------------|-------------------|
| Git Folder Integration   | ✅ Supported     | ❌ Not available   |
| DBC File Import          | ✅ Supported     | ✅ Supported       |
| Version Control Features | ✅ Full Git      | ❌ None            |
| Best Simplicity Option   | ✅ Either        | ✅ DBC Import      |

---

## Next Steps

After importing the materials:

- Open and run notebooks directly in the workspace
- Modify and experiment with code for hands-on learning
- Proceed with guided exercises in the course content

# Git Folders in Databricks

**Git folders** (formerly known as *Databricks Repos*) are specialized workspace directories that integrate directly with external Git repositories. They enable native support for Git-based version control within the Databricks environment. Supported providers include:

- GitHub (public, private, enterprise)
- GitLab (manual token setup)
- Azure DevOps

### Key Capabilities

- Clone remote repositories
- Create and manage branches
- Commit and push changes
- Pull remote updates
- Organize and version-control notebooks, scripts, and resources

Git folders enhance native notebook revision history by supporting:

- Persistent change tracking
- Collaborative workflows
- Branching and merging
- Source-controlled CI/CD

---

## Setting Up Git Integration

### Step 1: Open Git Account Settings

- Click the **User Profile** icon (top-right corner).
- Select **Settings**.
- In the left navigation, select **Linked Accounts**.

### Step 2: Select Git Provider

Databricks supports:

- **GitHub**
- **Azure DevOps**
- **GitLab** (requires manual token setup)

### Step 3: Link GitHub Account (Recommended)

#### Option 1: GitHub App (OAuth-based)

- Click **Link GitHub using GitHub App**.
- Approve Databricks via GitHub's OAuth interface.
- Grant repository access as prompted.

#### Option 2: Personal Access Token (Legacy)

- Generate a token from GitHub with appropriate scopes.
- Paste it into Databricks when prompted (less secure).

---

## Cloning a Git Repository

### Step 1: Create a Git Repository

In GitHub:

- Click **+** → **New repository**
- Name the repository (e.g., `DemoRepo`)
- Set visibility to **Private**
- Initialize with a **README**
- Click **Create repository**

### Step 2: Clone into Databricks

In Databricks:

- Copy the Git repository URL (e.g., `https://github.com/user/DemoRepo.git`)
- Go to the **Workspace** tab
- Click **Create** → **Git Folder**
- Paste the Git URL
- Click **Create Git Folder**

Databricks will:

- Detect the Git provider
- Create a folder linked to the repository
- Automatically check out the `main` branch

---

## Branch Management

### Creating a New Branch

- Click the current branch name (e.g., `main`)
- In the **Repos dialog**, click **Create Branch**
- Enter a branch name (e.g., `dev`)
- Click **Create**

The branch will be checked out immediately.

### Switching Branches

- Use the **branch dropdown** in the Git folder view
- Select any available branch

---

## Adding and Managing Content

### Adding Notebooks or Files

- Create folders or notebooks inside the Git folder
- Import files using the **three-dot menu** (`⋮`) → **Import**

### Cloning Notebooks into Git Folder

- In the **Workspace** tab, find the source notebook
- Click `⋮` → **Clone**
- Choose the Git folder as the destination path

---

## Committing and Pushing Changes

To commit changes:

1. Click the **branch name** to open the **Repos dialog**
2. Review the **Changed Files**
3. Enter a **commit message**
4. Click **Commit & Push**

Changes are committed locally and pushed to the remote branch.

---

## Pulling Changes from Remote

To sync with the remote repository:

1. Ensure the correct branch is selected
2. Open the **Repos dialog**
3. Click **Pull**

This downloads and applies the latest commits from the remote repository.

---

## Merging Branches via GitHub

To merge feature branches:

1. Go to GitHub and switch to the branch (e.g., `dev`)
2. Click **Contribute** → **Open Pull Request**
3. Review the changes
4. Click **Create Pull Request**
5. Click **Merge Pull Request** and confirm

Back in Databricks:

- Switch to the `main` branch
- Pull the latest changes to sync

---

## Summary: Git Folder Features

| Feature                   | Description                                |
|---------------------------|--------------------------------------------|
| Git integration           | Connect to GitHub, GitLab, or Azure DevOps |
| Commit & Push             | Save and upload changes from the UI        |
| Branch management         | Create, switch, and merge branches         |
| GitHub App support        | Secure OAuth-based linking                 |
| File import/export        | Add or clone notebooks into Git folders    |
| Pull remote updates       | Sync remote changes into Databricks        |
| Workspace sync            | Each Git folder maps 1:1 with a repository |
| Collaboration             | Multiple users can share a linked Git repo |

---

## Best Practices

- Use **feature branches** to isolate development
- Commit frequently with **descriptive messages**
- Avoid making direct changes in the `main` branch
- Perform **peer reviews** using pull requests
- Use the **GitHub App** for secure access control

---

- Git folders empower Databricks users with robust source control, enabling professional-grade code management and collaboration. 
- They are essential for maintaining clean workflows, ensuring reproducibility, and implementing CI/CD practices in data and analytics projects.

# Working with Databricks Notebooks

Databricks notebooks provide a collaborative, interactive interface for developing, testing, and executing data workflows. They support multi-language development, modular code execution, rich text documentation, and filesystem integration. Mastery of notebooks is essential for certification and day-to-day usage in Databricks environments.

---

## 1. Creating a New Notebook

To create a notebook:

- Navigate to the **Workspace** tab in the left sidebar.
- Click the **Create** button (top-right).
- Select **Notebook**.

A new notebook is created with a default name such as `Untitled Notebook`.

### Renaming the Notebook

- Click the notebook title.
- Enter a new name (e.g., `Notebook Basics`).

---

## 2. Language Support

Databricks notebooks support the following languages:

- **Python** (default)
- **SQL**
- **Scala**
- **R**

The default language can be set at creation. Individual cells can override this using **magic commands**.

---

## 3. Cluster Attachment

All notebook execution requires an active cluster:

- Use the **cluster dropdown** at the top of the notebook.
- Select the desired cluster (e.g., `Demo Cluster`).
- Click **Start** if the cluster is inactive.

The cluster status indicator turns green when ready.

---

## 4. Running Code Cells

To execute a code cell:

- Click the **Play** icon on the left of the cell.
- Or press `Shift + Enter`.

Additional actions:

- Run all cells above/below a selected cell
- Add new cells using the **"+"** icon

### Example

```python
print("Hello, World")
```

---

## 5. Language Magic Commands

Use magic commands to write different languages in a single notebook. Prefix the cell with a `%` directive.

### Examples

```sql
%sql
SELECT * FROM sales_data
```

```markdown
%md
## Markdown Header
This is a description paragraph.
```

> **Markdown** enables formatting for documentation including headers, bold, italics, lists, and embedded images.

---

## 6. Table of Contents (TOC)

The notebook auto-generates a table of contents from Markdown headers:

* Open the TOC using the **document icon** on the left toolbar.
* Click on section headers to navigate.

---

## 7. Modular Notebook Execution: `%run`

To import and execute another notebook:

1. Create a folder (e.g., `/Includes`)
2. Add a helper notebook (e.g., `Setup`)

### Setup Notebook (`/Includes/Setup`)

```python
# Setup values
full_name = "John Doe"
```

### Main Notebook

```python
%run /Includes/Setup
print(full_name)
```

> `%run` injects all definitions from the referenced notebook into the current context.

---

## 8. File System Operations

### Option 1: `%fs` (Magic Command)

```bash
%fs ls /databricks-datasets
```

Provides shell-style access to the Databricks File System (DBFS).

### Option 2: `dbutils.fs` (Programmatic Access)

```python
files = dbutils.fs.ls("/databricks-datasets")
display(files)
```

* `display()` renders data in a sortable table.
* Use for file exploration, ingestion, or listing.

### Helper Documentation

```python
dbutils.help()
dbutils.fs.help()
```

Provides descriptions for modules such as `fs`, `widgets`, and `secrets`.

---

## 9. Exporting and Importing Notebooks

### Export Options

* Open the **File menu** > **Export** > choose format:

  * `.ipynb` (iPython)
  * `.html`
* Export folders:

  * Use the **three-dot menu** (`⋮`) on a folder
  * Select **Export DBC Archive**

### Import Options

* Navigate to the **Workspace** tab.
* Click **Import** on the desired folder.
* Upload a `.dbc` or `.ipynb` file.

> **DBC Archives** package multiple notebooks/folders in a single file.

---

## 10. Revision History

Databricks automatically versions notebooks.

### Accessing Revisions

* Click the **"Last edit"** link at the top bar.
* Review the list of changes.
* Click **"Restore this revision"** to revert.

Use cases:

* Version comparison
* Undoing accidental changes
* Reviewing development history

---

## Summary of Features

| Feature                | Description                          |
| ---------------------- | ------------------------------------ |
| Multi-language support | Python, SQL, Scala, R                |
| Language switching     | `%sql`, `%md`, `%run`, `%fs`         |
| Cluster integration    | Required for execution               |
| File system access     | `%fs`, `dbutils.fs`                  |
| Table of contents      | Auto-generated from Markdown headers |
| Markdown support       | Rich-text formatting                 |
| Modular code sharing   | `%run` for importing notebooks       |
| Export formats         | `.ipynb`, `.dbc`, `.html`            |
| Import capability      | Upload `.ipynb` or `.dbc` files      |
| Revision tracking      | Built-in version history and restore |

---

Databricks notebooks offer a powerful, flexible environment for developing end-to-end data workflows. Their support for mixed-language scripting, built-in collaboration tools, and interactive visualization makes them a central component of the Databricks platform.
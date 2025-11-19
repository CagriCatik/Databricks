# Step-by-Step Guide - How to Configure Azure Databricks on VS Code

## Prerequisites

1. **Azure Subscription**: Ensure you have an active Azure subscription with access to Azure Databricks.
2. **Databricks Cluster**: Create an Azure Databricks workspace and cluster (instructions below).
3. **Azure CLI**: Make sure Azure CLI is installed and logged in.

## Step 1: Create an Azure Databricks Workspace and Cluster

1. Go to [Azure Portal](https://portal.azure.com/).
2. Navigate to **Azure Databricks** and create a new **workspace**.
3. Once the workspace is created, open it and go to **Clusters** > **Create Cluster**. Configure and start your cluster.

## Step 2: Install Required VS Code Extensions

1. **Python**: Install the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension if not already installed.
2. **Databricks Connect**: Install the [Databricks Connect](https://marketplace.visualstudio.com/items?itemName=databricks.databricks) extension from the VS Code marketplace.
3. **Jupyter Notebooks**: Install the [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extension if you plan to work with notebooks.

## Step 3: Install and Configure Databricks CLI

1. Open the **terminal** in VS Code and install the Databricks CLI:

   ```bash
   pip install databricks-cli
   ```

2. Authenticate and configure the CLI. Run the following command and enter your Databricks workspace details (token authentication is recommended):

   ```bash
   databricks configure --token
   ```

   - Enter **Databricks Host**: Obtain the workspace URL from the Azure Databricks portal.
   - Enter **Token**: Generate an access token from **User Settings** in Azure Databricks and paste it here.

## Step 4: Configure Databricks Connect

1. Ensure your cluster is running in Azure Databricks.
2. Install the Databricks Connect library on your local Python environment:

   ```bash
   pip install -U databricks-connect
   ```

3. Configure Databricks Connect with your cluster details:

   ```bash
   databricks-connect configure
   ```

   - Enter your **Databricks Host**, **Cluster ID**, and **Token**.
   - Set the **Org ID**: This is found in the workspace URL after `/o/`.
   - **Port**: Leave it as the default (usually `15001`).

4. Test the connection:

   ```bash
   databricks-connect test
   ```

   If successful, you should see connection information.

## Step 5: Use Databricks Connect in VS Code

1. **Create Python Scripts**: Write your code as you normally would in Python files (`.py`), and connect to your Databricks cluster.
2. **Submit Jobs**: Use the terminal in VS Code to submit your code as jobs on Databricks.

   ```bash
   databricks jobs create --json-file job.json
   ```

3. **Run and Test Notebooks**: For Jupyter notebooks, run code cells directly in VS Code, and they will execute on the connected Databricks cluster if configured correctly.

## Step 6: Debugging and Testing

1. **Remote Debugging**: To enable remote debugging, add `databricks-connect` as a remote interpreter in your Python settings.
2. **Testing**: Use `databricks-connect` to test Spark code locally with remote cluster resources, ensuring the compatibility of your code with Azure Databricks.

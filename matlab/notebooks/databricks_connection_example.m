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

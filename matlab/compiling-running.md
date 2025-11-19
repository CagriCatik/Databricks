# Compiling and Running a MATLAB Training Script on Databricks (Linux)

## Scope

Compile a MATLAB deep-learning training script into a Linux standalone executable with MATLAB Compiler, package it with MATLAB Runtime in a custom Docker image, run it on a Databricks cluster, and persist checkpoints to DBFS. References provided inline.

---

## Prerequisites

* MATLAB + MATLAB Compiler on a **Linux** build machine. Compiled artifacts are OS-specific. Build Linux for Linux. ([MathWorks][1])
* Access to MATLAB Runtime of the **same release** as the compiler. ([MathWorks][2])
* Databricks workspace with permission to run clusters and specify a **custom container image**. ([Databricks Dokumentation][3])

---

## Step 1: Refactor your training code for headless execution

Create an entry-point function (no GUI, no interactive figures). Save as `train_model.m`.

```matlab
function exit_code = train_model(dataPath, outPath)
% dataPath: directory with prepared training/validation data
% outPath: where to write logs, checkpoints, final model

% Example skeleton using Deep Learning Toolbox API
% Load data
imdsTrain = imageDatastore(fullfile(dataPath,"train"), "IncludeSubfolders",true, "LabelSource","foldernames");
imdsVal   = imageDatastore(fullfile(dataPath,"val"),   "IncludeSubfolders",true, "LabelSource","foldernames");

% Define net and training options (no plots)
lgraph = layerGraph(alexnet); % placeholder; replace with your model
opts = trainingOptions("sgdm", ...
    "MaxEpochs",5, ...
    "MiniBatchSize",64, ...
    "ValidationData",imdsVal, ...
    "Verbose",true, ...
    "Plots","none", ...
    "OutputFcn",@(info)checkpointFcn(info,outPath));

% Train
net = trainNetwork(imdsTrain, lgraph, opts);

% Save final artifact
if ~isfolder(outPath); mkdir(outPath); end
save(fullfile(outPath,"final_model.mat"),"net","-v7.3");

exit_code = 0;
end

function stop = checkpointFcn(info,outPath)
stop = false;
if info.State == "iteration" && mod(info.Iteration,100)==0
    if ~isfolder(outPath); mkdir(outPath); end
    save(fullfile(outPath, sprintf("ckpt_iter_%06d.mat", info.Iteration)), "-struct", "info");
end
end
```

Notes: MATLAB Compiler supports packaging command-line programs; compiled apps run under MATLAB Runtime without an interactive desktop. ([MathWorks][1])

---

## Step 2: Compile on a Linux build machine

Use `mcc` to create a **Linux** standalone. Example:

```bash
# From the folder containing train_model.m
mcc -m train_model.m -o train_model_cli
```

* `-m` builds a command-line executable; `-o` names the binary. See `mcc` reference for flags, including adding assets with `-a`. ([MathWorks][4])

The compiler also emits a helper script `run_train_model_cli.sh` that sets required environment variables before launching the binary with MATLAB Runtime. ([MathWorks][5])

---

## Step 3: Obtain and install MATLAB Runtime (Linux)

Download the **matching** Runtime and install silently:

```bash
# Example: place the MATLAB Runtime installer in /tmp/MATLAB_Runtime_R2024b_glnxa64
# Create a response file (installer control text)
cat >/tmp/mcr_silent.txt <<'EOF'
agreeToLicense=yes
destinationFolder=/opt/mcr
outputFile=/var/log/mcr_install.log
EOF

# Run installer silently
/tmp/MATLAB_Runtime_R2024b_glnxa64/install -mode silent -inputFile /tmp/mcr_silent.txt
```

* Silent/noninteractive options are documented for MATLAB Runtime installers. ([MathWorks][2])

---

## Step 4: Build a Databricks-ready Docker image

Create a minimalist image that contains:

* MATLAB Runtime (installed to `/opt/mcr`)
* Your compiled app artifacts (`train_model_cli`, `run_train_model_cli.sh`)
* Entrypoint convenience script

**Dockerfile (example):**

```dockerfile
FROM ubuntu:22.04

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libxext6 libxrender1 libxt6 libxi6 libxrandr2 libxfixes3 libxcursor1 \
    unzip curl bash && \
    rm -rf /var/lib/apt/lists/*

# Copy MATLAB Runtime installer payload and response file
# Expect these to be staged next to Dockerfile
COPY MATLAB_Runtime_R2024b_glnxa64 /tmp/MATLAB_Runtime_R2024b_glnxa64
COPY mcr_silent.txt /tmp/mcr_silent.txt

# Install MATLAB Runtime silently
RUN /tmp/MATLAB_Runtime_R2024b_glnxa64/install -mode silent -inputFile /tmp/mcr_silent.txt && \
    rm -rf /tmp/MATLAB_Runtime_R2024b_glnxa64 /tmp/mcr_silent.txt

# App files
WORKDIR /opt/app
COPY train_model_cli .
COPY run_train_model_cli.sh .

# Helper: wrapper that sets LD_LIBRARY_PATH then launches the app
RUN printf '%s\n' \
'#!/usr/bin/env bash' \
'export MCRROOT=/opt/mcr' \
'export LD_LIBRARY_PATH=$MCRROOT/v920/runtime/glnxa64:$MCRROOT/v920/bin/glnxa64:$MCRROOT/v920/sys/os/glnxa64:$LD_LIBRARY_PATH' \
'exec /opt/app/train_model_cli "$@"' > /usr/local/bin/run_train && \
    chmod +x /usr/local/bin/run_train

# Default working dir for jobs
WORKDIR /workdir
ENTRYPOINT ["/usr/local/bin/run_train"]
```

* Custom containers are the recommended way to standardize Databricks environments. ([Databricks Dokumentation][3])
* Setting the MATLAB Runtime library path at run time is required; MathWorks documents LD\_LIBRARY\_PATH usage for deployment. Replace `v920` with the correct version path for your Runtime. ([MathWorks][5])

Build and push:

```bash
docker build -t <registry>/<repo>/mcr-train:latest .
docker push <registry>/<repo>/mcr-train:latest
```

Databricks publishes reference container examples for guidance when adapting Dockerfiles. ([GitHub][6])

---

## Step 5: Create a Databricks cluster with this image

* In cluster configuration, specify the **custom Docker image** `<registry>/<repo>/mcr-train:latest`.
* Databricks Container Services docs cover setup, GPU notes, and init scripts if you need additional boot-time steps. ([Databricks Dokumentation][3])

If you must run shell configuration or mount commands at startup, use **init scripts**. ([Databricks Dokumentation][7], [Microsoft Learn][8])

---

## Step 6: Stage data and outputs on DBFS

Upload your prepared training data and pick an output directory:

```bash
# From your workstation using Databricks CLI (example)
databricks fs cp -r ./local_data dbfs:/mnt/data/myproject/train_data
```

You will pass `dataPath` and `outPath` pointing to **driver-visible** paths. In notebooks/shell on the cluster, paths under `/dbfs/...` map to DBFS. ([community.databricks.com][9])

---

## Step 7: Run the compiled training job on Databricks

From a Databricks notebook cell:

```bash
%sh
# Example invocation. The container ENTRYPOINT is /usr/local/bin/run_train.
# Map DBFS paths through /dbfs for the Linux process.
DATA_PATH=/dbfs/mnt/data/myproject/train_data
OUT_PATH=/dbfs/mnt/outputs/myproject/run_001

mkdir -p "$OUT_PATH"
run_train "$DATA_PATH" "$OUT_PATH"
```

You can also open the **Web Terminal** on the cluster’s driver to run shell commands interactively. ([Databricks Dokumentation][10], [Microsoft Learn][11], [Databricks][12])

---

## GPU acceleration (optional)

Use a GPU-enabled Databricks runtime and GPU nodes; ensure the CUDA/NVIDIA driver stack is compatible with your MATLAB release and Runtime. \[Inference]
Databricks documents running custom containers on GPU compute. ([Databricks Dokumentation][3])

---

## Parallelism and multi-node considerations

Compiled MATLAB apps execute as single processes by default. Multi-node or Spark-integrated workflows require MATLAB Parallel Server and specific Spark/cluster configuration; this is outside the standard compiled-app pattern for Databricks. ([MathWorks][13])

---

## Troubleshooting checklist

* Binary fails to start: verify **Runtime version** matches the build and **LD\_LIBRARY\_PATH** is set as documented for MATLAB Runtime. ([MathWorks][2])
* DBFS file access: invoke paths through `/dbfs/...` from shell; confirm permissions. ([community.databricks.com][9])
* Container boot customization: move repeated setup into **init scripts**. ([Databricks Dokumentation][7], [Microsoft Learn][8])

---

## References

* `mcc` reference (MATLAB Compiler). ([MathWorks][4])
* Standalone applications with MATLAB Compiler (platform-specific executables). ([MathWorks][1])
* Download and install MATLAB Runtime; silent/noninteractive options. ([MathWorks][2])
* Set MATLAB Runtime library path for deployment. ([MathWorks][5])
* Databricks custom containers (Docker) for clusters, including GPU notes. ([Databricks Dokumentation][3])
* Databricks container examples (reference Dockerfiles). ([GitHub][6])
* Databricks init scripts documentation. ([Databricks Dokumentation][7], [Microsoft Learn][8])
* MATLAB Parallel Server on Spark/Databricks (advanced, optional). ([MathWorks][13])

[1]: https://www.mathworks.com/help/compiler/standalone-applications.html "Standalone Applications - MATLAB & Simulink - MathWorks"
[2]: https://www.mathworks.com/help/compiler/install-the-matlab-runtime.html "Download and Install MATLAB Runtime - MATLAB & Simulink - MathWorks"
[3]: https://docs.databricks.com/aws/en/compute/custom-containers "Customize containers with Databricks Container Service"
[4]: https://www.mathworks.com/help/compiler/mcc.html "mcc - Compile MATLAB functions for deployment - MATLAB - MathWorks"
[5]: https://www.mathworks.com/help/compiler/mcr-path-settings-for-run-time-deployment.html "Set MATLAB Runtime Path for Deployment - MATLAB & Simulink - MathWorks"
[6]: https://github.com/databricks/containers "Databricks Container Services - Example Containers - GitHub"
[7]: https://docs.databricks.com/aws/en/init-scripts/ "What are init scripts? | Databricks Documentation"
[8]: https://learn.microsoft.com/en-us/azure/databricks/init-scripts/ "What are init scripts? - Azure Databricks | Microsoft Learn"
[9]: https://community.databricks.com/t5/data-engineering/how-to-execute-sh-and-py-file-in-the-workspace/td-p/28995 "How to execute .sh and .py file in the workspace? - Databricks"
[10]: https://docs.databricks.com/aws/en/compute/web-terminal "Run shell commands in Databricks web terminal | Databricks Documentation"
[11]: https://learn.microsoft.com/en-us/azure/databricks/compute/web-terminal "Run shell commands in Azure Databricks web terminal"
[12]: https://www.databricks.com/blog/2020/08/31/introducing-the-databricks-web-terminal.html "Introducing Databricks Web Terminal | Databricks Blog"
[13]: https://www.mathworks.com/help/matlab-parallel-server/configure-a-spark-cluster.html "Configure for Spark Clusters - MATLAB & Simulink - MathWorks"

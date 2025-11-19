# syntax=docker/dockerfile:1
# check=skip=all

## Dockerfile to build MATLAB Container where:
# 1. Base image is Databricks Runtime
# 2. MATLAB R2025b using MATLAB Package Manager & install dependencies from mathworks-ref-arch/container-images repository

### Dockerfile Build Commands:

# By Default the container will be built for Databricks Runtime 16.4-LTS and Ubuntu 24.04.
# docker build -t matlab-on-databricks:R2025b-16.4  .

# To build the container for a different Databricks Runtime version or Ubuntu version, you can use the following commands:
# docker build --build-arg DATABRICKS_IMAGE_TAG=15.4-LTS \
#              --build-arg UBUNTU_VERSION=22.04 \
#              -t matlab-on-databricks:R2025b-15.4  .

# The other build arguments can be used to specify the MATLAB release, product list, install location, and license server.
# For example, to build the container with MATLAB R2025b, a specific product list, and a license server, you can use the following command:
# docker build --build-arg MATLAB_RELEASE=R2025b \
#              --build-arg MATLAB_PRODUCT_LIST="MATLAB Deep_Learning_Toolbox Symbolic_Math_Toolbox" \
#              --build-arg MATLAB_INSTALL_LOCATION="/opt/matlab/R2025b" \
#              --build-arg LICENSE_SERVER=12345@hostname.com \
#              -t my_matlab_image_name .

# Specify the Databricks Runtime version to use as the base image.
ARG DATABRICKS_IMAGE_TAG=16.4-LTS
# Specify the version of Ubuntu used in the base image.
ARG UBUNTU_VERSION=24.04
# Use the python that is recommended by Databricks: https://docs.databricks.com/aws/en/compute/custom-containers#option-1-use-a-base-built-by-databricks
ARG PYTHON3=/databricks/python3/bin/python3
# Specify the MATLAB release to install.
ARG MATLAB_RELEASE=R2025b
# Specify the list of products(toolboxes) to install into MATLAB.
ARG MATLAB_PRODUCT_LIST="MATLAB Simulink"
# Specify MATLAB Install Location.
ARG MATLAB_INSTALL_LOCATION="/opt/matlab/${MATLAB_RELEASE}"

# Specify license server information using the format: port@hostname
ARG LICENSE_SERVER
ARG NLM=${LICENSE_SERVER:+"-with-nlm"}

#################################################################################################
## Build stage that installs MATLAB and its dependencies.
#################################################################################################

FROM databricksruntime/standard:${DATABRICKS_IMAGE_TAG} AS base
ARG UBUNTU_VERSION
ARG PYTHON3
ARG MATLAB_RELEASE
ARG MATLAB_INSTALL_LOCATION
ARG MATLAB_PRODUCT_LIST

USER root

RUN [ -d /usr/share/X11/xkb ] || mkdir -p /usr/share/X11/xkb

ARG MATLAB_DEPS_URL="https://raw.githubusercontent.com/mathworks-ref-arch/container-images/main/matlab-deps/${MATLAB_RELEASE}/ubuntu${UBUNTU_VERSION}/base-dependencies.txt"
ARG MATLAB_DEPENDENCIES="matlab-deps-${MATLAB_RELEASE}-base-dependencies.txt"
# gettext is required for the administer-mathworks-service-host/admin-scripts/linux/admin-controlled-installation/install.sh script to run
ARG ADDITIONAL_PACKAGES="wget curl unzip ca-certificates xvfb git vim gettext fluxbox"

# Configure Python (>3.12) to allow installing system wide packages.
ENV PIP_BREAK_SYSTEM_PACKAGES=1

## Install dependencies
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update \
    && apt-get install --no-install-recommends -y ${ADDITIONAL_PACKAGES} \
    && wget $(echo ${MATLAB_DEPS_URL} | tr "[:upper:]" "[:lower:]") -O ${MATLAB_DEPENDENCIES} \
    && xargs -a ${MATLAB_DEPENDENCIES} -r apt-get install --no-install-recommends -y \
    && apt-get clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/* ${MATLAB_DEPENDENCIES}

WORKDIR /matlab-install
ARG MSH_MANAGED_INSTALL_ROOT=/usr/local/MathWorks/ServiceHost/
ARG MSH_DOWNLOAD_LOCATION=/tmp/Downloads/MathWorks/ServiceHost
## Install MATLAB & Administered MathWorks Service Host
# Note: Installation of Support Packages, requires MPM to run as end user.
RUN wget -q https://www.mathworks.com/mpm/glnxa64/mpm \
    && chmod +x mpm \
    && ./mpm install \
    --release=${MATLAB_RELEASE} \
    --destination=${MATLAB_INSTALL_LOCATION} \
    --products ${MATLAB_PRODUCT_LIST} \
    || (echo "MPM Installation Failure. See below for more information:" && cat /tmp/mathworks_root.log && false) \
    && rm -rf mpm /tmp/mathworks_root.log \
    && ln -s ${MATLAB_INSTALL_LOCATION}/bin/matlab /usr/local/bin/matlab \
    && git clone https://github.com/mathworks-ref-arch/administer-mathworks-service-host.git \
    && cd /matlab-install/administer-mathworks-service-host/admin-scripts/linux/admin-controlled-installation \
    && ./download_msh.sh --destination ${MSH_DOWNLOAD_LOCATION} \
    && ./install_msh.sh --source ${MSH_DOWNLOAD_LOCATION} --destination ${MSH_MANAGED_INSTALL_ROOT} --no-update-environment \
    && ./cleanup_default_msh_installation_location.sh --for-all-users \
    && cd / && rm -rf /matlab-install ${MSH_DOWNLOAD_LOCATION}

# Work dir assumed by Databricks
WORKDIR /root

ENV MATHWORKS_SERVICE_HOST_MANAGED_INSTALL_ROOT=${MSH_MANAGED_INSTALL_ROOT}

########################################################################
# Install matlab-proxy as root user for all users of the container
########################################################################
## MATLAB Proxy Configuration
ENV MW_CONTEXT_TAGS=MATLAB_PROXY:DATABRICKS:V1
ENV MWI_USE_COOKIE_CACHE=True
ENV MWI_APP_PORT=8888
ENV MWI_BASE_URL="/matlab"
# Disabling Token Authentication, as Databricks already has several layers of authentication built into it.
ENV MWI_ENABLE_TOKEN_AUTH=False
EXPOSE 8888

RUN ${PYTHON3} -m pip install --no-cache-dir matlab-proxy

#######################################################################
# Install MATLAB Engine for Python
# Installation can fail if, Python Version is incompatible.
# For more information, see https://mathworks.com/support/requirements/python-compatibility.html
#
# Failure to install does not stop the build
########################################################################
RUN echo "Installing MATLAB Engine for Python..." && \
    MATLAB_VERSION=$(cat ${MATLAB_INSTALL_LOCATION}/VersionInfo.xml | grep -oP '(\d{2}\.\d{1})') && \
    env LD_LIBRARY_PATH=${MATLAB_INSTALL_LOCATION}/bin/glnxa64 ${PYTHON3} -m pip install --no-cache-dir matlabengine==${MATLAB_VERSION}.* || \
    echo "Failed to install MATLAB Engine for Python... skipping ..."

# Reset PIP settings
ENV PIP_BREAK_SYSTEM_PACKAGES=

#################################################################################################
## Build stage that sets the LICENSE_SERVER information only if provided at build time.
#################################################################################################
FROM base AS base-with-nlm
ARG LICENSE_SERVER
RUN echo "Setting MLM_LICENSE_FILE to ${LICENSE_SERVER}"
ENV MLM_LICENSE_FILE=${LICENSE_SERVER}

#################################################################################################
## Final stage that sets the entrypoint and exposes the MATLAB Proxy application.
#################################################################################################
FROM base${NLM} AS final

# Entrypoint supposed to be ignored in Databricks and can be used for local testing.
# ENTRYPOINT ["/bin/sh", "-c", "su ubuntu -c 'cd $HOME && . /databricks/python3/bin/activate && matlab-proxy-app'" ]

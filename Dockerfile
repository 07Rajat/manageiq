# Use the official Jenkins LTS image with explicit platform
FROM --platform=linux/amd64 jenkins/jenkins:lts

# Switch to root user to install packages
USER root

# Install required packages
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        libssl-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        libjpeg-dev \
        libpng-dev \
        wget \
        unzip \
        curl \
        jq \
        libfontconfig1 \
        libfreetype6 \
        libx11-6 \
        libxcb1 \
        libxext6 \
        libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Install Terraform
ARG TERRAFORM_VERSION=1.5.0
RUN mkdir -p /usr/local/bin && \
    wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -O /tmp/terraform.zip && \
    unzip /tmp/terraform.zip -d /usr/local/bin && \
    rm /tmp/terraform.zip

# Install oc CLI
RUN curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz && \
    tar -xzf openshift-client-linux.tar.gz && \
    mv oc /usr/local/bin/ && \
    rm openshift-client-linux.tar.gz README.md

# Ensure proper permissions
RUN chown -R jenkins:jenkins /var/jenkins_home && \
    chmod 755 /usr/local/bin/jenkins.sh

# Switch to the existing Jenkins user
USER jenkins

# Set the working directory
WORKDIR /var/jenkins_home

# Expose the Jenkins port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Set the entrypoint to start Jenkins
ENTRYPOINT ["/bin/sh", "-c", "exec /usr/local/bin/jenkins.sh"]
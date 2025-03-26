FROM --platform=linux/amd64 jenkins/jenkins:lts

USER root

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

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

ARG TERRAFORM_VERSION=1.5.0
RUN mkdir -p /usr/local/bin && \
    wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -O /tmp/terraform.zip && \
    unzip /tmp/terraform.zip -d /usr/local/bin && \
    rm /tmp/terraform.zip

RUN curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz && \
    tar -xzf openshift-client-linux.tar.gz && \
    mv oc /usr/local/bin/ && \
    rm openshift-client-linux.tar.gz README.md

RUN chown -R jenkins:jenkins /var/jenkins_home && \
    chmod 755 /usr/local/bin/jenkins.sh

USER jenkins

WORKDIR /var/jenkins_home

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "-c", "exec /usr/local/bin/jenkins.sh"]
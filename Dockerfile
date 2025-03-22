FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    make \
    cmake \
    zlib1g-dev \
    libjpeg-turbo8-dev \
    libfreetype6-dev \
    python3 \
    python3-venv \
    python3-pip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Set the working directory
WORKDIR /opt/scripts

# Default command (can be overridden when running the container)
CMD ["python3", "--version"]
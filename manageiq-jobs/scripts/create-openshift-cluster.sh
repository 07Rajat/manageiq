#!/bin/bash

# Function to display messages
msg() {
  echo >&2 -e "${1-}"
}

# Function to handle errors
die() {
  local msg=$1
  local code=${2:-1} # default return code is 1
  msg "$msg"
  exit "${code}"
}

# Function to display usage
usage() {
cat <<EOF
    Usage: $(basename "${BASH_SOURCE[0]}") [-h] [options]

    This script creates an OpenShift cluster on IBM Cloud.

    Available options:
    -i, --ibm-api-key     IBM Cloud API key
    -r, --repo-url        Git repository URL for Terraform code
EOF
  exit
}

# Function to parse parameters
parse_params() {
  while :; do
    case "${1-}" in
    -h | --help) usage ;;
    -i | --ibm-api-key)
      IBM_API_KEY="${2-}"
      shift
      ;;
    -r | --repo-url)
      REPO_URL="${2-}"
      shift
      ;;
    -?*) die "Unknown option: $1" ;;
    *) break ;;
    esac
    shift
  done

  args=("$@")

  # Check required parameters
  [[ -z "${IBM_API_KEY-}" ]] && die "Missing --ibm-api-key parameter"
  [[ -z "${REPO_URL-}" ]] && die "Missing --repo-url parameter"
  return 0
}

# Main function
function main() {
  # Parse parameters
  parse_params "$@"

  # Clone or update the Terraform repository
  if [ -d "terraform-repo" ]; then
    msg "Updating existing Terraform repository..."
    cd terraform-repo
    git pull || die "Failed to update repository"
  else
    msg "Cloning Terraform repository..."
    git clone "${REPO_URL}" terraform-repo || die "Failed to clone repository"
    cd terraform-repo
  fi

  # Navigate to the Terraform directory
  cd terraform-repo/ibm-cloud || die "Failed to navigate to IBM Cloud Terraform directory"

  # Initialize and apply Terraform
  msg "Executing Terraform for IBM Cloud..."
  terraform init || die "Terraform init failed for IBM Cloud"

  # Create Terraform resources
  msg "creating Terraform resources..."
  terraform apply -auto-approve -var="ibm_api_key=${IBM_API_KEY}" || die "Terraform apply failed for IBM Cloud"

  msg "Terraform execution completed successfully!"
}

# Call the main function
main "$@"
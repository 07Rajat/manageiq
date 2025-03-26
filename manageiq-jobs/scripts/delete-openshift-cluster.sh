#!/bin/bash

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2-1}
  msg "$msg"
  exit "${code}"
}

usage() {
cat <<EOF
    Usage: $(basename "${BASH_SOURCE[0]}") [-h] [options]

    This script deletes an OpenShift cluster on IBM Cloud.

    Available options:
    -i, --ibm-api-key     IBM Cloud API key
    -r, --repo-url        Git repository URL for Terraform code
EOF
  exit
}

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

  [[ -z "${IBM_API_KEY-}" ]] && die "Missing --ibm-api-key parameter"
  [[ -z "${REPO_URL-}" ]] && die "Missing --repo-url parameter"
  return 0
}

# Main function
function main() {
  
  parse_params "$@"

  if [ -d "terraform-repo" ]; then
    msg "Updating existing Terraform repository..."
    cd terraform-repo
    git pull || die "Failed to update repository"
  else
    msg "Cloning Terraform repository..."
    git clone "${REPO_URL}" terraform-repo || die "Failed to clone repository"
    cd terraform-repo
  fi

  cd ibm-cloud || die "Failed to navigate to IBM Cloud Terraform directory"

  msg "Initializing Terraform..."
  terraform init || die "Terraform init failed"

  msg "Destroying Terraform resources..."
  terraform destroy -auto-approve -var="ibm_api_key=${IBM_API_KEY}" || die "Terraform destroy failed"

  msg "Terraform destruction completed successfully!"
}

main "$@"
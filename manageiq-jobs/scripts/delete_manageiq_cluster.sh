#!/bin/bash

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2:-1}
  msg "$msg"
  exit "${code}"
}

usage() {
cat <<EOF
    Usage: $(basename "${BASH_SOURCE[0]}") [-h] [options]

    This script add OCP cluster entry to ManageIQ.

    Available options:
    -n, --clustername     Name of the cluster
    -m, --mqserver        MQ Server
    -t, --mquser          Name of the MQ user
    -r, --mqpass          MQ Server password
EOF
  exit
}

parse_params() {
  while :; do
    case "${1-}" in
    -h | --help) usage ;;
    -n | --clustername)
      CLUSTER_NAME="${2-}"
      shift
      ;;
    -m | --mqserver)
      MQ_SERVER="${2-}"
      shift
      ;;
    -t | --mquser)
      MQUSER="${2-}"
      shift
      ;;
    -r | --mqpass)
      MQPASS="${2-}"
      shift
      ;;	
    -?*) die "Unknown option: $1" ;;
    *) break ;;
    esac
    shift
  done

  args=("$@")

  [[ -z "${CLUSTER_NAME-}" ]] && die "Missing --clustername parameter"
  [[ -z "${MQ_SERVER}" ]] && die "Missing --mqserver parameter"
  [[ -z "${MQUSER-}" ]] && die "Missing --mquser parameter"
  [[ -z "${MQPASS-}" ]] && die "Missing --mqpass parameter"
  return 0
}

function main() {

    echo $CLUSTER_NAME

    id=$(curl --user $MQUSER:$MQPASS --insecure --request GET --header "Content-Type: application/json" ${MQ_SERVER}/api/providers --get --data "expand=resources" --data "filter[]=name='$CLUSTER_NAME'" | jq -r '.resources[].id')
    echo "deleting entry from manageiq with id:$id"

    curl --user $MQUSER:$MQPASS --insecure --request DELETE ${MQ_SERVER}/api/providers/${id}
    returnCode=$?
    if [[ ${returnCode} != 0 ]]; then
      log.error "Cluster deletion failed with returnCode: ${returnCode}"
      exit 1
    fi
}

parse_params "$@"
main

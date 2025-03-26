#!/bin/bash

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2:-1} # default return code is 1
  msg "$msg"
  exit "${code}"
}

usage() {
cat <<EOF
    Usage: $(basename "${BASH_SOURCE[0]}") [-h] [options]

    This script add OCP cluster entry to ManageIQ.

    Available options:
    -n, --clustername     Name of the cluster
    -u, --username        Username for OCP cluster
    -p, --password        Password for OCP cluster
    -s, --server          Name of OCP url
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
    -u | --username)
      USERNAME="${2-}"
      shift
      ;;
    -p | --password)
      PASSWORD="${2-}"
      shift
      ;;
    -s | --server)
      OCP_URL="${2-}"
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
  [[ -z "${USERNAME-}" ]] && die "Missing --username parameter"
  [[ -z "${PASSWORD-}" ]] && die "Missing --password parameter"
  [[ -z "${OCP_URL-}" ]] && die "Missing --server parameter"
  [[ -z "${MQ_SERVER}" ]] && die "Missing --mqserver parameter"
  [[ -z "${MQUSER-}" ]] && die "Missing --mquser parameter"
  [[ -z "${MQPASS-}" ]] && die "Missing --mqpass parameter"
  return 0
}

function main() {

    PROJECT_NAME="management-manageiq"
    SERVICE_ACCOUNT_NAME="management-admin"


    HOSTNAME=$(echo $OCP_URL | awk -F'://' '{print $2}' | awk -F':' '{print $1}')

    echo $HOSTNAME

    PORT=$(echo $OCP_URL | awk -F'://' '{print $2}' | awk -F':' '{print $2}')

    echo $PORT

    echo "oc login -u $USERNAME -p $PASSWORD $OCP_URL"
    oc login -u $USERNAME -p $PASSWORD $OCP_URL
    echo "oc login -u ${USERNAME} -p ${PASSWORD} ${OCP_URL}"
    oc login -u ${USERNAME} -p ${PASSWORD} ${OCP_URL}
    echo "oc login --server=${OCP_URL} --insecure-skip-tls-verify=true -u ${USERNAME} -p ${PASSWORD}"
    oc login --server="${OCP_URL}" --insecure-skip-tls-verify=true -u "${USERNAME}" -p "${PASSWORD}"

    oc adm new-project $PROJECT_NAME --description="ManageIQ Project"

    oc create serviceaccount $SERVICE_ACCOUNT_NAME -n $PROJECT_NAME

    echo '{"apiVersion": "authorization.openshift.io/v1", "kind": "ClusterRole", "metadata": {"name": "management-manageiq-admin"}, "rules": [{"resources": ["pods/proxy"], "verbs": ["*"]}]}' | oc create -f -

    oc policy add-role-to-user -n $PROJECT_NAME admin -z $SERVICE_ACCOUNT_NAME
    oc policy add-role-to-user -n $PROJECT_NAME management-manageiq-admin -z $SERVICE_ACCOUNT_NAME
    oc adm policy add-cluster-role-to-user cluster-reader system:serviceaccount:$PROJECT_NAME:$SERVICE_ACCOUNT_NAME
    oc adm policy add-scc-to-user privileged system:serviceaccount:$PROJECT_NAME:$SERVICE_ACCOUNT_NAME
    oc adm policy add-cluster-role-to-user self-provisioner system:serviceaccount:$PROJECT_NAME:$SERVICE_ACCOUNT_NAME

    TOKEN_NAME=$(oc describe sa -n $PROJECT_NAME $SERVICE_ACCOUNT_NAME | grep "Tokens:" | awk -F' ' '{print $2}')

    TOKEN=$(oc describe secret -n $PROJECT_NAME $TOKEN_NAME | grep "token:" | awk -F' ' '{print $2}')

    METRICS_ROUTE=$(oc get routes -n openshift-monitoring | grep prometheus-k8s-openshift-monitoring | awk -F' ' '{print $2}')

    # Add Cluster entry to manageIQ
    curl --user $MQUSER:$MQPASS --insecure --request POST ${MQ_SERVER}/api/providers -d '{"action":"create","name":"'${CLUSTER_NAME}'","port":'${PORT}',"type":"ManageIQ::Providers::Openshift::ContainerManager","hostname":"'${HOSTNAME}'","connection_configurations":[{"endpoint":{"role":"default","security_protocol":"ssl-without-validation","verify_ssl":0},"authentication":{"authtype":"bearer","type":"AuthToken","auth_key":"'${TOKEN}'"}},{"endpoint": {"role": "prometheus","hostname": "'${METRICS_ROUTE}'","port": 443,"security_protocol":"ssl-without-validation"}}]}'
    returnCode=$?
    if [[ ${returnCode} != 0 ]]; then
      echo "returnCode: $returnCode"
      exit 1
    fi
}

parse_params "$@"
main

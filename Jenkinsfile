pipeline {
    agent any

    parameters {
        choice(name: 'ACTION', choices: ['add', 'delete'], description: 'Choose to add or delete a cluster')
        string(name: 'CLUSTER_NAME', defaultValue: '', description: 'Name of the cluster')
        string(name: 'USERNAME', defaultValue: '', description: 'OpenShift username')
        string(name: 'PASSWORD', defaultValue: '', description: 'OpenShift password')
        string(name: 'OCP_URL', defaultValue: '', description: 'OpenShift API URL')
        string(name: 'MQ_SERVER', defaultValue: '', description: 'ManageIQ server URL')
        string(name: 'MQUSER', defaultValue: '', description: 'ManageIQ username')
        string(name: 'MQPASS', defaultValue: '', description: 'ManageIQ password')
        string(name: 'PROJECT_NAME', defaultValue: 'management-manageiq', description: 'OpenShift project name')
        string(name: 'SERVICE_ACCOUNT_NAME', defaultValue: 'management-admin', description: 'Service account name')
    }

    environment {
        CLUSTER_NAME = "${params.CLUSTER_NAME}"
        USERNAME = "${params.USERNAME}"
        PASSWORD = "${params.PASSWORD}"
        OCP_URL = "${params.OCP_URL}"
        MQ_SERVER = "${params.MQ_SERVER}"
        MQ_USER = "${params.MQUSER}"
        MQ_PASS = "${params.MQPASS}"
        PROJECT_NAME = "${params.PROJECT_NAME}"
        SERVICE_ACCOUNT_NAME = "${params.SERVICE_ACCOUNT_NAME}"
    }

    stages {
        stage('Run Script') {
            steps {
                script {
                    if (params.ACTION == 'add') {
                        echo "Running 'add' job..."
                        echo "Cluster name is ${CLUSTER_NAME}"
                        sh "./scripts/add_cluster.sh -n ${CLUSTER_NAME} -u ${USERNAME} -p ${PASSWORD} -s ${OCP_URL} -m ${MQ_SERVER} -t ${MQ_USER} -r ${MQ_PASS}"
                    } else if (params.ACTION == 'delete') {
                        echo "Running 'delete' job..."
                        sh "./scripts/delete_cluster.sh"
                    } else {
                        error "Invalid action selected. Choose 'add' or 'delete'."
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Job completed successfully!"
        }
        failure {
            echo "Job failed. Check the logs for details."
        }
    }
}

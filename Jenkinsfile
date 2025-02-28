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

    stages {
        stage('Run Script') {
            steps {
                script {
                    
                    def clusterName = params.CLUSTER_NAME
                    def username = params.USERNAME
                    def password = params.PASSWORD
                    def ocpUrl = params.OCP_URL
                    def mqServer = params.MQ_SERVER
                    def mqUser = params.MQUSER
                    def mqPass = params.MQPASS

                    if (params.ACTION == 'add') {
                        echo "Running 'add' job..."
                        echo "Cluster name is ${clusterName}"
                        sh "./scripts/add_cluster.sh -n ${clusterName} -u ${username} -p ${password} -s ${ocpUrl} -m ${mqServer} -t ${mqUser} -r ${mqPass}"
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

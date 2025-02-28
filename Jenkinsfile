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
                    if (params.ACTION == 'add') {
                        echo "Running 'add' job..."
                        echo "Cluster name is ${params.CLUSTER_NAME}"
                        // Ensure script is executable before running
                        sh """
                        pwd
                        chmod +x ./manageiq-jobs/scripts/add_cluster.sh
                        ./manageiq-jobs/scripts/add_cluster.sh -n ${params.CLUSTER_NAME} -u ${params.USERNAME} -p ${params.PASSWORD} -s ${params.OCP_URL} -m ${params.MQ_SERVER} -t ${params.MQUSER} -r ${params.MQPASS}
                        """
                    } else if (params.ACTION == 'delete') {
                        echo "Running 'delete' job..."
                        sh """
                        chmod +x ./manageiq-jobs/scripts/delete_cluster.sh
                        ./manageiq-jobs/scripts/delete_cluster.sh
                        """
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

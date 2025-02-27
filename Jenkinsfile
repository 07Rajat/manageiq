// properties([
//     parameters([
//         string(name: 'CLUSTER_NAME', defaultValue: '', description: 'Name of the OCP Cluster. Eg:fusion-devops-1 (Mandatory)'),
//         booleanParam(name: 'IS_IBM_CLOUD_CLUSTER', defaultValue: false, description: 'Select true if this is IBM Cloud Cluster'),
//         string(name: 'USERNAME', defaultValue: '', description: 'Username for OCP Cluster'),
//         password(name: 'PASSWORD', description: 'Password or Token for OCP console. Eg: WEC7q-zs7qM-P4iJa-XXXX or sha256~H5bvxz4H7gpXXa3PkYW-jehe2J27d-XXXXXXXXX (Mandatory)'),
//         string(name: 'OCP_API_URL', defaultValue: '', description: 'OCP API url, leave it blank if cluster type is IBM ROKS'),
//         string(name: 'MANAGEIQ_SERVER_URL', defaultValue: 'https://manageiq-sample.apps.dragon-isd-sre.g4c0.p1.openshiftapps.com', description: 'ManageIQ url')
// ])
// ])

// // This is needed to make the creds available for underlying scripts 
// withCredentials([usernamePassword(credentialsId: 'git-access-token', usernameVariable: '', passwordVariable: 'GITHUB_TOKEN')
                
//                 ]
//                 )
// {
//     env.GITHUB_TOKEN = GITHUB_TOKEN
    
// }

// timeout(time: 180, unit: 'MINUTES') {
//    node("") {
//    checkout scm

//       stage("ManageIQ entry"){
//       // Add cluster entry to ManageIQ server
//       buildName("$CLUSTER_NAME")
//       def MANAGEIQ_USER = "admin"
//       def MANAGEIQ_PASS = "smartvm"
//       sh """#!/bin/bash
//         if [[ $IS_IBM_CLOUD_CLUSTER == "true" ]]
//         then
//             export OCP_ENVIRONMENT="IBM_ROKS"
//             ibmcloud login --apikey $PASSWORD
//             ibmcloud oc cluster config -c $CLUSTER_NAME
//             export OCP_API_URL=\$(ibmcloud oc cluster get -c $CLUSTER_NAME |grep "Public Service Endpoint URL:"| awk -F' ' '{print \$5}')
//             echo "OCP_API_URL=\$OCP_API_URL"
//             #add-manageiq.sh -n $env.CLUSTER_NAME -u $env.USERNAME -p $env.PASSWORD -s \$OCP_API_URL -m $env.MANAGEIQ_SERVER_URL -t $MANAGEIQ_USER -r $MANAGEIQ_PASS
//         else
//             echo "OCP_API_URL=\$OCP_API_URL"
//             add-manageiq.sh -n $env.CLUSTER_NAME -u $env.USERNAME -p $env.PASSWORD -s $env.OCP_API_URL -m $env.MANAGEIQ_SERVER_URL -t $MANAGEIQ_USER -r $MANAGEIQ_PASS
//         fi
//       """
//       } 
//    }
// }


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
        // Define environment variables for the scripts
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
                        echo 'cluster name is $env.CLUSTER_NAME'
                        sh './scripts/add_cluster.sh -n $env.CLUSTER_NAME -u $env.USERNAME -p $env.PASSWORD -s $env.OCP_URL -m $env.MQ_SERVER -t $MQ_USER -r $MQ_PASS'
                        //sh './scripts/add_cluster.sh'
                    } else if (params.ACTION == 'delete') {
                        echo "Running 'delete' job..."
                        sh './scripts/delete_cluster.sh'
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
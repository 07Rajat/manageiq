# Centralized Platform For Cluster Allocation And Access In OpenShift HCI

## Overview

### This project automates the creation and management of OpenShift clusters using Jenkins, Terraform, and MongoDB for resource tracking.

1. The pipeline:

2. Clones the required repositories (manageiq and terraform-repo).

3. Fetches allocated resource details from MongoDB.

4. Validates if requested resources are available.

5. Initializes Terraform for provisioning.

6. Updates MongoDB with new resource allocations.


## Technologies Used

1. Jenkins: Automates the pipeline execution.

2. Terraform: Manages OpenShift cluster infrastructure.

3. MongoDB: Stores allocated resources.

4. Python: Handles resource fetching and updates.

5. Bash: Executes script automation.
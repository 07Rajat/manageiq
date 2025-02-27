# manageiq
Manageiq Project 

## PR-Triggered Jenkins Jobs

- When a PR is raised, Jenkins will automatically detect the changes and trigger the appropriate job.
- If changes are made to `scripts/add_cluster.sh`, the **create** job will run.
- If changes are made to `scripts/delete_cluster.sh`, the **delete** job will run.
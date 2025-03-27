---
name: "ManageIQ/OpenShift Request"
about: "Request creation or deletion of resources"
title: "[Request] [Type] for [Team]"
labels: "infrastructure, manageiq, request"
assignees: ""
---

### **Request Type**  
- [ ] **Create ManageIQ Instance**  
- [ ] **Delete ManageIQ Instance**  
- [ ] **Create OpenShift Cluster**  
- [ ] **Delete OpenShift Cluster**    

### **Requester Information**  
| Field              | Value                        |
|--------------------|------------------------------|
| **Team Name**      | _e.g., Data Analytics Team_  |
| **Contact Person** | _@mention / email_           |
| **Urgency**        | Low / Medium / High          |
| **JIRA Ticket** | Associated tracking ticket (if any) | "PROJ-1234" |

### **ManageIQ Instance Details**  
| Field                 | Value                        |
|-----------------------|------------------------------|
| **Cluster Name**      | _e.g., `miq-team1-prod`_     |
| **Cloud Provider**    | AWS / IBM / GCP / Azure      |
| **ManageIQ Server URL**| _e.g., `https://miq.example.com`_ |
| **Cluster URL**       | _e.g., `https://cluster.example.com`_ |

### **OpenShift Cluster Details** _(if applicable)_  
| Field                     | Value                          |
|---------------------------|--------------------------------|
| **Cluster Name**          | _e.g., `ocp-team1-dev`_        |
| **K8s Version**           | _e.g., 4.12_                   |
| **Worker Nodes**          | _e.g., 3_                      |
| **Requested CPU per Node**| _e.g., 8 Cores_                |
| **Requested Memory per Node** | _e.g., 32GB RAM_           |
| **Storage per Node**      | _e.g., 200GB_                  |
| **Networking**           | Ingress, CIDR, VPN, etc.       |

### **Justification**  
> Briefly explain the purpose (e.g., new project, testing, decommissioning).  

### **Approval**  
- [ ] **Approved by** `@infra-team`  
- [ ] **Pending Review**  
- [ ] **Rejected** (Reason: _____)
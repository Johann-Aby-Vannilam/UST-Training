# Enterprise AWS 3-Tier Web Architecture Documentation

---

<img width="1536" height="1024" alt="End to end request flow" src="https://github.com/user-attachments/assets/8478930b-3c55-4bb2-bafd-6d8036324a05" />


---
## Project Overview

This project implements a production-style highly available 3-tier web architecture on AWS using a custom VPC design, public and private subnet segmentation, dual Application Load Balancers, security group chaining, reverse proxy architecture, Node.js application services, and MySQL database integration.

The architecture follows enterprise cloud design principles including:

* Network segmentation
* High availability
* Least privilege access
* Layered security
* Internal service communication
* Reverse proxy routing
* Private subnet isolation
* Load balancing
* Horizontal scalability
* Operational troubleshooting practices

---

<img width="1024" height="1536" alt="Volume 5a" src="https://github.com/user-attachments/assets/80fd55bb-6161-4a9f-b254-f7d30592a979" />


---

# 1. Architecture Overview

## High-Level Flow

```text
Internet
↓
Public Application Load Balancer
↓
Web Tier (Nginx + React Frontend)
↓
Internal Application Load Balancer
↓
Application Tier (Node.js + PM2)
↓
Database Tier (MySQL)
```

---

# 2. AWS Services Used

| AWS Service               | Purpose                                     |
| ------------------------- | ------------------------------------------- |
| Amazon VPC                | Network isolation and segmentation          |
| EC2                       | Compute instances for Bastion, Web, App, DB |
| Application Load Balancer | Layer 7 HTTP traffic routing                |
| Auto Scaling Group        | Horizontal scaling and HA                   |
| Internet Gateway          | Public internet connectivity                |
| NAT Gateway               | Outbound internet for private instances     |
| Route Tables              | Network routing                             |
| Security Groups           | Stateful firewall controls                  |
| IAM                       | Administrative access control               |
| CloudShell / AWS CLI      | Infrastructure management                   |

---

# 3. VPC Design

## VPC Information

| Configuration | Value          |
| ------------- | -------------- |
| VPC Name      | Production-VPC |
| CIDR Block    | 10.0.0.0/16    |
| Region        | us-east-1      |

### Design Rationale

A /16 CIDR range was selected to:

* Support future subnet expansion
* Enable scalable multi-tier segmentation
* Follow enterprise IP planning practices

---

# 4. Subnet Architecture

## Public Subnets

| Subnet          | CIDR        | AZ         | Purpose                |
| --------------- | ----------- | ---------- | ---------------------- |
| Public-Subnet-1 | 10.0.1.0/24 | us-east-1a | ALB, Bastion, Web Tier |
| Public-Subnet-2 | 10.0.2.0/24 | us-east-1b | ALB, Web Tier          |

### Components Hosted

* Public Application Load Balancer
* Bastion Host
* Web Tier EC2 Instances
* NAT Gateway

---

## Application Private Subnets

| Subnet           | CIDR        | AZ         | Purpose  |
| ---------------- | ----------- | ---------- | -------- |
| Private-Subnet-1 | 10.0.3.0/24 | us-east-1a | App Tier |
| Private-Subnet-2 | 10.0.4.0/24 | us-east-1b | App Tier |

### Components Hosted

* Internal Application Load Balancer
* Node.js Application Instances

### Security Characteristics

* No direct internet access
* Reachable only through internal routing
* Protected behind Internal ALB

---

## Database Private Subnets

| Subnet      | CIDR        | AZ         | Purpose        |
| ----------- | ----------- | ---------- | -------------- |
| DB-Subnet-1 | 10.0.5.0/24 | us-east-1a | MySQL Database |
| DB-Subnet-2 | 10.0.6.0/24 | us-east-1b | Future HA DB   |

### Security Characteristics

* Fully isolated database network
* No public access
* Accessible only from App Tier SG

---

# 5. Availability Zone Strategy

The architecture was distributed across:

* us-east-1a
* us-east-1b

### Purpose

* High Availability
* Fault Tolerance
* Multi-AZ resiliency
* Load distribution

This prevents single AZ failure from impacting the entire application stack.

---

# 6. Internet Connectivity

## Internet Gateway

| Component        | Name     |
| ---------------- | -------- |
| Internet Gateway | Prod-IGW |

### Purpose

Provides:

* Public internet access
* External HTTP connectivity
* Public ALB accessibility
* Bastion SSH access

---

## NAT Gateway

| Component   | Name       |
| ----------- | ---------- |
| NAT Gateway | Production |

### Purpose

Allows private subnet resources to:

* Install packages
* Download dependencies
* Access repositories
* Perform outbound internet communication

Without exposing private instances publicly.

---

# 7. Route Table Design

## Public Route Table

| Route     | Target           |
| --------- | ---------------- |
| 0.0.0.0/0 | Internet Gateway |

### Associated Subnets

* Public-Subnet-1
* Public-Subnet-2

---

## Private Route Table

| Route     | Target      |
| --------- | ----------- |
| 0.0.0.0/0 | NAT Gateway |

### Associated Subnets

* Private-Subnet-1
* Private-Subnet-2

---

## Database Route Table

Dedicated DB route table used for:

* Database isolation
* Future segmentation
* Security enhancement
* Enterprise zoning practices

---

# 8. Security Architecture

## Security Model

The environment follows:

* Least privilege access
* Layered security
* Security group chaining
* Internal-only service communication

---

## Bastion Security Group

### Inbound Rules

| Port | Source           | Purpose    |
| ---- | ---------------- | ---------- |
| 22   | Administrator IP | SSH access |

### Purpose

Provides secure administrative access into private infrastructure.

---

## Web Tier Security Group

### Inbound Rules

| Port | Source        | Purpose            |
| ---- | ------------- | ------------------ |
| 80   | Public ALB SG | Web traffic        |
| 22   | Bastion SG    | SSH administration |

### Purpose

Secures frontend web servers.

---

## Internal ALB Security Group

### Inbound Rules

| Port | Source      | Purpose              |
| ---- | ----------- | -------------------- |
| 4000 | Web Tier SG | Internal API routing |

### Purpose

Controls internal communication between Web and App tiers.

---

## App Tier Security Group

### Inbound Rules

| Port | Source          | Purpose                     |
| ---- | --------------- | --------------------------- |
| 4000 | Internal ALB SG | Backend application traffic |
| 22   | Bastion SG      | SSH administration          |

### Purpose

Protects backend application services.

---

## Database Security Group

### Inbound Rules

| Port | Source      | Purpose               |
| ---- | ----------- | --------------------- |
| 3306 | App Tier SG | MySQL database access |

### Purpose

Ensures database is accessible only from application servers.

---

# 9. Compute Layer

## Bastion Host

### Purpose

* Administrative jump server
* Secure SSH access into private subnets

### Characteristics

* Public subnet deployment
* Controlled SSH access
* Centralized administration point

---

# 10. Web Tier

## Technologies Used

* React.js
* Nginx
* Node.js

## Responsibilities

* Serve frontend application
* Reverse proxy API requests
* Route API calls to Internal ALB
* Handle static content delivery

---

## Nginx Reverse Proxy Architecture

### API Flow

```text
/api/*
↓
Internal ALB :4000
↓
App Tier
```

### Purpose

* Hide internal infrastructure
* Enable secure backend routing
* Centralize frontend/backend integration

---

## React Frontend Deployment

### Build Process

```bash
npm install
npm run build
```

### Deployment Path

```text
/var/www/html
```

### Served Through

* Nginx Web Server

---

# 11. Public Application Load Balancer

| Configuration | Value           |
| ------------- | --------------- |
| Name          | Web-ALB         |
| Type          | Internet-facing |
| Listener      | HTTP :80        |
| Target Group  | Web Tier        |

### Responsibilities

* External user entry point
* Traffic distribution
* High availability routing
* Health checks

---

# 12. Application Tier

## Technologies Used

* Node.js
* Express.js
* PM2
* mysql2 driver

---

## Responsibilities

* Business logic processing
* REST API services
* Database interaction
* Transaction management

---

## API Endpoints

| Endpoint     | Method | Purpose               |
| ------------ | ------ | --------------------- |
| /health      | GET    | Health validation     |
| /transaction | GET    | Retrieve transactions |
| /transaction | POST   | Insert transaction    |
| /transaction | DELETE | Delete transactions   |

---

## PM2 Process Management

### Purpose

* Process resiliency
* Automatic restart
* Background execution
* Service persistence

### Commands Used

```bash
pm2 start index.js --name app-tier
pm2 save
pm2 startup
```

---

# 13. Internal Application Load Balancer

| Configuration | Value      |
| ------------- | ---------- |
| Name          | App-LB     |
| Type          | Internal   |
| Listener      | HTTP :4000 |
| Target Group  | App Tier   |

### Purpose

* Internal service routing
* Load balancing backend APIs
* Secure east-west traffic management

---

# 14. Database Tier

## Technology Used

* MySQL

## Deployment Model

* EC2-hosted database
* Private subnet deployment

---

## Database Configuration

| Configuration | Value        |
| ------------- | ------------ |
| Database      | webappdb     |
| Table         | transactions |

---

## Table Structure

```sql
CREATE TABLE IF NOT EXISTS transactions(
    id INT NOT NULL AUTO_INCREMENT,
    amount DECIMAL(10,2),
    description VARCHAR(100),
    PRIMARY KEY(id)
);
```

---

# 15. High Availability Design

## HA Components

| Layer        | HA Strategy            |
| ------------ | ---------------------- |
| Public Layer | Multi-AZ ALB           |
| Web Tier     | Multiple EC2 instances |
| App Tier     | Multiple EC2 instances |
| Routing      | Health checks          |
| Networking   | Multi-AZ subnets       |

---

# 16. Auto Scaling Preparation

## Web Tier AMI

Created reusable AMI from healthy Web Tier instance.

### Purpose

* Rapid scaling
* Immutable infrastructure
* Consistent deployments

---

## Launch Template

Configured with:

* Web Tier AMI
* Security Group
* Instance type
* Key pair

---

## Auto Scaling Group

### Purpose

* Automatic scaling
* Self-healing infrastructure
* High availability

### Scaling Characteristics

* Minimum instances: 2
* Desired instances: 2
* Maximum instances: 4

---

# 17. Troubleshooting Activities Performed

## Infrastructure Debugging

Resolved:

* Security group misconfigurations
* ALB target registration issues
* Health check failures
* Route connectivity problems
* Internal ALB listener mismatches

---

## Application Debugging

Resolved:

* React build failures
* Nginx reverse proxy issues
* PM2 startup issues
* Backend connectivity failures
* MySQL authentication incompatibility

---

## Database Debugging

Resolved:

* MySQL authentication protocol mismatch
* Node.js mysql driver incompatibility

### Solution

Migrated:

```text
mysql
→
mysql2
```

---

# 18. Security Best Practices Implemented

| Practice                 | Implemented |
| ------------------------ | ----------- |
| Private subnet isolation | Yes         |
| Bastion architecture     | Yes         |
| Security group chaining  | Yes         |
| Internal ALB             | Yes         |
| DB isolation             | Yes         |
| Multi-tier segmentation  | Yes         |
| Least privilege access   | Yes         |

---

# 19. Enterprise Design Principles Demonstrated

## Layered Architecture

* Presentation Tier
* Application Tier
* Database Tier

---

## Network Segmentation

* Public zone
* Application zone
* Database zone

---

## Internal Service Communication

Implemented secure:

```text
Web Tier → Internal ALB → App Tier
```

architecture.

---

## High Availability

Implemented:

* Multi-AZ deployment
* Load balancing
* Health monitoring
* Fault tolerance

---

# 20. Final Architecture Flow

```text
Internet
↓
Public Application Load Balancer
↓
Web Tier EC2 Instances
(Nginx + React)
↓
Internal Application Load Balancer
↓
App Tier EC2 Instances
(Node.js + PM2)
↓
MySQL Database Tier
```

---

# 21. Project Outcome

Successfully implemented a production-style AWS 3-tier web architecture featuring:

* Secure VPC networking
* Public and private subnet segregation
* Reverse proxy architecture
* Internal and external load balancing
* Highly available application routing
* Backend API services
* Database integration
* Auto scaling readiness
* Enterprise-grade security patterns
* Real-world operational troubleshooting

The environment demonstrates practical enterprise cloud architecture principles suitable for scalable and secure application deployment on AWS.

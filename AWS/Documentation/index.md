# Enterprise AWS 3-Tier Architecture Documentation

## Production-Style Highly Available AWS Infrastructure Implementation

---

# Document Information

| Field              | Value                                         |
| ------------------ | --------------------------------------------- |
| Project Title      | Enterprise AWS 3-Tier Architecture            |
| Cloud Platform     | Amazon Web Services (AWS)                     |
| Architecture Type  | Highly Available Multi-Tier Web Architecture  |
| Deployment Model   | Production-Style Infrastructure               |
| Documentation Type | Enterprise Cloud Infrastructure Documentation |
| Region Used        | us-east-1                                     |
| Domain Used        | b4n3xus.in                                    |

---

# Purpose of This Documentation

This documentation provides a complete theoretical and practical explanation of designing, implementing, securing, scaling, and troubleshooting a production-style AWS 3-tier architecture.

The document is designed for:

* Beginners learning cloud computing and AWS
* Students studying enterprise cloud architecture
* Engineers learning AWS networking and infrastructure
* Professionals understanding scalable cloud deployments
* Infrastructure and DevOps learning purposes

The documentation combines:

* Cloud computing fundamentals
* AWS service explanations
* Networking concepts
* Security architecture
* High availability design
* Scalability implementation
* Practical infrastructure deployment
* Real-world troubleshooting
* Enterprise best practices

---

# Architecture Overview

## High-Level Architecture Flow

```text
Internet
↓
Public Application Load Balancer
↓
Web Tier EC2 Instances
(Nginx + React Frontend)
↓
Internal Application Load Balancer
↓
Application Tier EC2 Instances
(Node.js + PM2)
↓
MySQL Database EC2
```

---

# Core Architecture Principles Implemented

The environment was designed following enterprise cloud engineering principles.

## Key Principles

### 1. Multi-Tier Architecture

The infrastructure separates the application into multiple layers:

* Presentation Layer
* Application Layer
* Database Layer

This improves:

* Security
* Scalability
* Maintainability
* Fault isolation
* Traffic management

---

### 2. Network Segmentation

The infrastructure uses isolated network zones:

* Public subnet layer
* Private application subnet layer
* Isolated database subnet layer

This reduces exposure and improves security.

---

### 3. High Availability

The infrastructure is distributed across multiple Availability Zones.

Implemented HA strategies include:

* Multi-AZ deployment
* Load balancing
* Health checks
* Auto Scaling preparation
* Redundant application instances

---

### 4. Least Privilege Security

The environment follows a layered security model using:

* Security Groups
* Bastion Host access
* Private subnet isolation
* Internal load balancing
* Controlled east-west traffic communication

---

### 5. Scalability

The architecture supports horizontal scaling using:

* AMIs
* Launch Templates
* Auto Scaling Groups
* Load Balancer target groups

---

# Documentation Structure

This documentation is divided into multiple enterprise-style volumes.

---

# Volume 1 — Cloud & AWS Foundations

## Topics Covered

### Chapter 1 — Introduction to Cloud Computing

* What is cloud computing
* Traditional infrastructure vs cloud infrastructure
* Advantages of cloud computing
* CAPEX vs OPEX
* Elasticity and scalability
* Shared responsibility model

---

### Chapter 2 — Cloud Service Models

* IaaS
* PaaS
* SaaS
* Real-world examples
* AWS service mapping

---

### Chapter 3 — AWS Global Infrastructure

* Regions
* Availability Zones
* Edge locations
* AWS global network
* Fault tolerance concepts

---

### Chapter 4 — Networking Fundamentals

* IP addressing
* Public IP vs Private IP
* CIDR notation
* Subnetting basics
* Routing fundamentals
* NAT concepts
* TCP/IP overview
* Ports and protocols
* HTTP vs HTTPS

---

### Chapter 5 — DNS Fundamentals

* What is DNS
* How DNS works
* DNS resolution flow
* Recursive resolver
* Root servers
* TLD servers
* Authoritative DNS
* Domain names

---

# Volume 2 — AWS Networking, Security & IAM

## Topics Covered

### Chapter 1 — Amazon VPC

* What is a VPC
* Why VPC is required
* VPC CIDR planning
* Enterprise VPC design
* Custom VPC implementation

---

### Chapter 2 — Subnet Architecture

* Public subnets
* Private subnets
* Database subnets
* Multi-tier subnet segmentation
* Multi-AZ subnet design

---

### Chapter 3 — Route Tables & Routing

* Route tables
* Static routing
* Default routes
* Internet routing
* Private routing
* Database routing isolation

---

### Chapter 4 — Internet Gateway & NAT Gateway

* Internet Gateway architecture
* Public internet connectivity
* NAT Gateway concepts
* Private outbound internet access
* Secure internet communication for private instances

---

### Chapter 5 — Security Groups

* Stateful firewall concepts
* Security group chaining
* Layered security
* SG-to-SG communication
* Inbound and outbound rules
* Enterprise firewall design

---

### Chapter 6 — Bastion Host Architecture

* What is a Bastion Host
* Why Bastion Hosts are required
* Secure administrative access
* SSH management strategy
* Jump server architecture

---

### Chapter 7 — IAM Fundamentals

* What is IAM
* IAM users
* IAM groups
* IAM policies
* Administrative access
* Least privilege principle
* MFA concepts
* IAM best practices

### Practical Implementation

* Created IAM user
* Assigned AdministratorAccess policy
* Used IAM credentials for infrastructure management

---

# Volume 3 — Load Balancing, Traffic Routing & Scalability

## Topics Covered

### Chapter 1 — Load Balancing Fundamentals

* What is a Load Balancer
* Why Load Balancers are required
* Traffic distribution
* High availability
* Fault tolerance
* Health checks

---

### Chapter 2 — AWS Load Balancer Types

* Application Load Balancer (ALB)
* Network Load Balancer (NLB)
* Gateway Load Balancer (GWLB)
* Classic Load Balancer (CLB)

---

### Chapter 3 — Application Load Balancer Deep Dive

* Layer 7 routing
* HTTP request inspection
* Listener concepts
* Rules and priorities
* Default actions
* Target groups
* Health checks

---

### Chapter 4 — ALB Routing Rules & Conditions

* Host-based routing
* Path-based routing
* Listener conditions
* Rule priority evaluation
* Header-based routing
* Query-string routing
* Source IP conditions

### Practical Learning Performed

* Listener rule experimentation
* Host-based routing implementation
* Path-based routing implementation
* Traffic forwarding analysis

---

### Chapter 5 — Reverse Proxy Concepts

* What is a reverse proxy
* Nginx reverse proxy architecture
* API forwarding
* Backend abstraction
* Request routing
* Frontend/backend separation

### Implemented Architecture

```text
/api/*
↓
Internal ALB
↓
Application Tier
```

---

### Chapter 6 — Internal Load Balancer Architecture

* Internal ALB concepts
* East-west traffic management
* Internal service communication
* Private backend routing
* Backend service isolation

---

### Chapter 7 — High Availability

* What is High Availability
* Fault tolerance
* Multi-AZ architecture
* Redundancy
* Self-healing systems
* Enterprise HA strategies

---

### Chapter 8 — Auto Scaling

* Horizontal scaling
* Vertical scaling
* Dynamic scaling
* Scaling policies
* Auto Scaling Groups
* Launch Templates
* AMI concepts

### Practical Implementation

| Configuration    | Value |
| ---------------- | ----- |
| Minimum Capacity | 2     |
| Desired Capacity | 2     |
| Maximum Capacity | 4     |

---

# Volume 4 — DNS & Route 53

## Topics Covered

### Chapter 1 — Domain Name System (DNS)

* DNS fundamentals
* Domain resolution process
* Public DNS architecture
* DNS records
* DNS propagation

---

### Chapter 2 — Route 53 Fundamentals

* What is Route 53
* Hosted zones
* Public hosted zones
* DNS management
* Route 53 integration with AWS services

---

### Chapter 3 — DNS Record Types

* A Records
* AAAA Records
* CNAME Records
* Alias Records
* MX Records
* TXT Records

---

### Chapter 4 — Alias vs CNAME

* Differences between Alias and CNAME
* AWS-native Alias records
* ALB DNS integration
* Best practices

---

### Chapter 5 — Practical DNS Implementation - 3 tier application

## Domain Used

```text
b4n3xus.in
```

### Implementations Performed

* Domain integration
* Subdomain creation
* A records
* CNAME records
* Alias records
* ALB domain mapping

---

# Volume 5 — Enterprise AWS 3-Tier Case Study

# Production-Style Highly Available AWS Infrastructure Implementation

---

## Chapter 1 — Project Objective

The goal of this project was to design and implement a production-style highly available AWS infrastructure capable of securely hosting a modern multi-tier web application.

The environment was designed to demonstrate:

* Enterprise VPC architecture
* Secure subnet segmentation
* Internal and external load balancing
* Reverse proxy architecture
* High availability principles
* Horizontal scalability
* Secure database isolation
* Operational troubleshooting

---

## Chapter 2 — AWS Services Used

| AWS Service               | Purpose                     |
| ------------------------- | --------------------------- |
| Amazon VPC                | Network isolation           |
| EC2                       | Compute infrastructure      |
| Application Load Balancer | Traffic distribution        |
| Auto Scaling Group        | Scalability and HA          |
| Internet Gateway          | Public connectivity         |
| NAT Gateway               | Private outbound internet   |
| Route Tables              | Traffic routing             |
| Security Groups           | Firewall security           |
| IAM                       | Identity and access control |
| Route 53                  | DNS management              |

---

## Chapter 3 — VPC Architecture

| Configuration | Value          |
| ------------- | -------------- |
| VPC Name      | Production-VPC |
| CIDR Block    | 10.0.0.0/16    |
| Region        | us-east-1      |

### Design Decisions

The VPC was designed with:

* Multi-tier segmentation
* Multi-AZ resiliency
* Dedicated security zones
* Future scalability support

---

## Chapter 4 — Subnet Architecture

### Public Subnets

| Subnet          | CIDR        | AZ         | Purpose                |
| --------------- | ----------- | ---------- | ---------------------- |
| Public-Subnet-1 | 10.0.1.0/24 | us-east-1a | ALB, Bastion, Web Tier |
| Public-Subnet-2 | 10.0.2.0/24 | us-east-1b | ALB, Web Tier          |

---

### Application Private Subnets

| Subnet           | CIDR        | AZ         | Purpose  |
| ---------------- | ----------- | ---------- | -------- |
| Private-Subnet-1 | 10.0.3.0/24 | us-east-1a | App Tier |
| Private-Subnet-2 | 10.0.4.0/24 | us-east-1b | App Tier |

---

### Database Private Subnets

| Subnet      | CIDR        | AZ         | Purpose   |
| ----------- | ----------- | ---------- | --------- |
| DB-Subnet-1 | 10.0.5.0/24 | us-east-1a | Database  |
| DB-Subnet-2 | 10.0.6.0/24 | us-east-1b | Future HA |

---

## Chapter 5 — Security Architecture

### Security Layers

The environment implemented:

* Bastion access control
* Private subnet isolation
* Security group chaining
* Internal ALB architecture
* Controlled east-west communication

---

### Security Group Communication Flow

```text
Public ALB SG
↓
Web Tier SG
↓
Internal ALB SG
↓
App Tier SG
↓
Database SG
```

---

## Chapter 6 — Request Flow Analysis

```text
Internet
↓
Public ALB
↓
Web Tier
↓
Internal ALB
↓
Application Tier
↓
Database Tier
```

### Flow Explanation

1. Users access the application through the public ALB.
2. Traffic is distributed to the web tier instances.
3. Nginx forwards API traffic internally.
4. Internal ALB routes backend requests.
5. Application servers process business logic.
6. Database queries are executed securely in private subnets.

---

## Chapter 7 — High Availability Strategy

### Implemented HA Components

| Layer         | Strategy               |
| ------------- | ---------------------- |
| Load Balancer | Multi-AZ deployment    |
| Web Tier      | Multiple EC2 instances |
| App Tier      | Multiple EC2 instances |
| Routing       | Health checks          |
| Scaling       | Auto Scaling readiness |

---

## Chapter 8 — Scalability Design

### Scaling Components

* AMI creation
* Launch Templates
* Auto Scaling Group
* ALB target groups
* Health checks

### Auto Scaling Configuration

| Parameter | Value |
| --------- | ----- |
| Minimum   | 2     |
| Desired   | 2     |
| Maximum   | 4     |

---

## Chapter 9 — Operational Learnings

### Key Areas Learned

* AWS networking
* Layered cloud security
* Load balancing
* High availability
* Reverse proxy architecture
* Infrastructure troubleshooting
* Private networking
* DNS integration
* Internal service communication

---



# Final Conclusion

This project successfully implemented a production-style highly available AWS 3-tier infrastructure demonstrating:

* Enterprise VPC design
* Multi-tier cloud architecture
* Secure networking
* Private subnet isolation
* Internal and external load balancing
* High availability principles
* Horizontal scalability preparation
* Bastion host administration
* DNS integration
* Real-world troubleshooting
* Enterprise cloud engineering practices

The implementation provides strong practical understanding of AWS infrastructure engineering, networking, scalability, and operational troubleshooting in enterprise cloud environments.

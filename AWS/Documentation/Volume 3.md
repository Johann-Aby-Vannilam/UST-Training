# Volume 3 — Load Balancing, Traffic Routing & Scalability

---

# Chapter 1 — Load Balancing Fundamentals

Modern applications receive traffic from:

* users
* mobile apps
* APIs
* browsers
* third-party systems

As traffic increases, a single server becomes insufficient because:

* performance degrades
* downtime risk increases
* failures affect all users
* scalability becomes limited

Load Balancers solve these problems by:

* distributing traffic
* improving availability
* increasing scalability
* enabling fault tolerance
* monitoring application health

This chapter explains:

* what a Load Balancer is
* why Load Balancers are required
* traffic distribution
* high availability
* fault tolerance
* health checks
* practical implementation from this project

---

# 1. What is a Load Balancer

---

# Definition

A Load Balancer is a system that distributes incoming traffic across multiple backend servers.

Instead of sending all traffic to a single server:

* requests are distributed intelligently

This improves:

* performance
* scalability
* availability
* fault tolerance

---

# Simple Explanation

Without a Load Balancer:

```text id="sd9t8n"
Users
↓
Single Server
```

All traffic reaches one server.

If the server:

* crashes
* becomes overloaded

the application fails.

---

# With a Load Balancer

```text id="zlmtr7"
Users
↓
Load Balancer
↓
Server 1
Server 2
Server 3
```

Traffic is distributed across multiple servers.

---

# Real-World Analogy

Imagine a supermarket with multiple billing counters.

Without traffic distribution:

* everyone waits in one queue

With multiple counters:

* customers are distributed efficiently

A Load Balancer works similarly for application traffic.

---

# Load Balancer in This Project

The architecture implemented:

* Public Application Load Balancer
* Internal Application Load Balancer

Used for:

* frontend traffic distribution
* backend service routing
* high availability
* internal communication

---

# High-Level Traffic Flow

```text id="xqm4dj"
User
↓
Public ALB
↓
Web Tier
↓
Internal ALB
↓
App Tier
```

---

# 2. Why Load Balancers Are Required

---

# Problem Without Load Balancers

If all traffic reaches a single server:

* CPU usage increases
* memory becomes overloaded
* application crashes become likely
* downtime affects all users

---

# Enterprise Traffic Challenges

Modern applications may receive:

* thousands of concurrent users
* unpredictable traffic spikes
* global traffic loads

A single server cannot reliably handle this.

---

# Load Balancer Solution

Load Balancers:

* distribute traffic
* reduce server overload
* improve performance
* increase availability

---

# Example

Without Load Balancer:

```text id="d9c0r5"
1000 Users
↓
1 Server
```

Potential result:

* overload
* downtime

---

# With Load Balancer

```text id="1m6t0z"
1000 Users
↓
Load Balancer
↓
Multiple Servers
```

Traffic is shared efficiently.

---

# Enterprise Benefits of Load Balancers

| Benefit           | Explanation                          |
| ----------------- | ------------------------------------ |
| Scalability       | Handle increasing traffic            |
| High Availability | Avoid single points of failure       |
| Fault Tolerance   | Redirect traffic from failed servers |
| Performance       | Balanced workload                    |
| Flexibility       | Dynamic backend scaling              |

---

# Why Load Balancers Were Used in This Project

The architecture required:

* Multi-AZ deployment
* scalable traffic distribution
* backend isolation
* internal application routing
* future Auto Scaling support

Load Balancers enabled all these capabilities.

---

# 3. Traffic Distribution

---

# What is Traffic Distribution

Traffic distribution means:

* spreading requests across multiple backend servers

instead of overloading a single instance.

---

# Traffic Distribution Flow

```text id="v6t3bo"
Users
↓
Load Balancer
↓
Web Server 1
Web Server 2
Web Server 3
```

---

# Why Traffic Distribution Is Important

Benefits:

* reduced server overload
* improved response time
* better scalability
* balanced resource usage

---

# Traffic Distribution in This Project

The Public ALB distributed traffic to:

* multiple Web Tier instances

The Internal ALB distributed traffic to:

* backend App Tier instances

---

# Multi-AZ Traffic Distribution

```text id="7twwt7"
ALB
↓
AZ-1 Web Server
AZ-2 Web Server
```

Traffic was distributed across:

* Availability Zones
* backend targets

---

# Load Balancing Algorithms

Different Load Balancers use different algorithms.

Common examples:

* Round Robin
* Least Connections
* Weighted Routing

AWS ALB primarily distributes traffic dynamically based on:

* target availability
* connection handling

---

# Benefits of Traffic Distribution

| Benefit                  | Explanation               |
| ------------------------ | ------------------------- |
| Better Performance       | Reduced server load       |
| Improved Availability    | Multiple targets          |
| Efficient Resource Usage | Balanced workload         |
| Horizontal Scaling       | Add more instances easily |

---

# 4. High Availability

---

# What is High Availability

High Availability (HA) means:

* applications remain operational
* even during failures

---

# Why HA Is Important

Downtime affects:

* users
* businesses
* revenue
* reliability

Enterprise systems must minimize downtime.

---

# Load Balancers and HA

Load Balancers improve HA by:

* distributing traffic
* avoiding single-server dependency
* routing to healthy instances

---

# HA Architecture in This Project

The infrastructure used:

* Multi-AZ deployment
* redundant servers
* Load Balancers
* health checks

---

# Multi-AZ High Availability

```text id="n2u8ja"
ALB
↓
AZ-1 Instance
AZ-2 Instance
```

If one AZ fails:

* traffic continues to healthy targets.

---

# Enterprise Importance of HA

Industries requiring HA:

* banking
* healthcare
* streaming platforms
* e-commerce
* financial systems

---

# Example

If one web server crashes:

* ALB redirects traffic to healthy servers automatically.

Users experience:

* minimal downtime

---

# 5. Fault Tolerance

---

# What is Fault Tolerance

Fault tolerance means:

* systems continue functioning
* even when components fail

---

# Difference Between HA and Fault Tolerance

| Concept           | Meaning                           |
| ----------------- | --------------------------------- |
| High Availability | Minimize downtime                 |
| Fault Tolerance   | Continue operating during failure |

---

# Fault Tolerance Using Load Balancers

Load Balancers:

* detect failed instances
* stop sending traffic to unhealthy targets
* continue routing to healthy servers

---

# Fault Tolerance Flow

```text id="evrm1s"
Server 1 → Failed
↓
ALB removes failed target
↓
Traffic sent to healthy servers
```

---

# Fault Tolerance in This Project

Implemented using:

* ALB
* Multi-AZ deployment
* multiple EC2 instances
* health checks

---

# Why Fault Tolerance Matters

Without fault tolerance:

* single server failure causes downtime

Enterprise systems avoid:

# single points of failure

---

# 6. Health Checks

---

# What are Health Checks

Health checks monitor backend server health.

Load Balancers periodically verify:

* whether instances are healthy
* whether applications respond correctly

---

# Why Health Checks Are Important

Without health checks:

* traffic may still route to failed servers

This causes:

* errors
* downtime
* failed requests

---

# Health Check Flow

```text id="tkn3nm"
ALB
↓
Health Check Request
↓
Backend Server
↓
Healthy / Unhealthy Status
```

---

# Health Checks in This Project

The ALBs monitored:

* web servers
* backend app servers

using:

* HTTP health checks

---

# Example Health Check

```text id="ywb6n8"
HTTP GET /
Port 80
```

---

# Healthy vs Unhealthy Targets

| Status    | Meaning         |
| --------- | --------------- |
| Healthy   | Traffic allowed |
| Unhealthy | Traffic blocked |

---

# Automatic Failure Handling

If a target becomes unhealthy:

* ALB removes it automatically

Traffic continues to:

* healthy instances only

---

# Enterprise Importance of Health Checks

Health checks improve:

* availability
* resilience
* automated recovery
* fault tolerance

---

# Practical Example in This Project

Suppose:

* Web Server 1 fails

The ALB:

* detects failed health checks
* stops routing traffic to that instance
* continues routing to healthy targets

---

# Load Balancer Concepts Used in This Project

| Concept              | Implementation          |
| -------------------- | ----------------------- |
| Public ALB           | Internet-facing traffic |
| Internal ALB         | Backend communication   |
| Traffic Distribution | Multi-instance routing  |
| High Availability    | Multi-AZ deployment     |
| Fault Tolerance      | Health-based routing    |
| Health Checks        | HTTP target monitoring  |

---

# Complete Traffic Architecture

```text id="sl2vtq"
User
↓
Public ALB
↓
Web Tier
↓
Internal ALB
↓
App Tier
↓
Database
```

---

# Enterprise Design Principles Implemented

| Principle            | Implementation          |
| -------------------- | ----------------------- |
| High Availability    | Multi-AZ infrastructure |
| Scalability          | Multi-instance routing  |
| Fault Tolerance      | Health checks           |
| Security             | Internal ALB            |
| Layered Architecture | Multi-tier routing      |

---

# Summary

Load Balancers are essential components of modern cloud infrastructure.

This chapter explained:

* Load Balancer fundamentals
* traffic distribution
* high availability
* fault tolerance
* health checks
* scalable architecture design

These concepts enabled:

* resilient application delivery
* Multi-AZ traffic distribution
* automated failure handling
* scalable enterprise architecture

# Chapter 2 — AWS Load Balancer Types

AWS provides multiple types of Load Balancers designed for different networking and application requirements.

Each Load Balancer type is optimized for:

* different traffic patterns
* protocol handling
* scalability requirements
* application architectures

Choosing the correct Load Balancer is extremely important because it directly affects:

* performance
* scalability
* latency
* traffic routing
* availability
* application design

This chapter explains:

* Application Load Balancer (ALB)
* Network Load Balancer (NLB)
* Gateway Load Balancer (GWLB)
* Classic Load Balancer (CLB)
* enterprise use cases
* practical implementation from this project

---

# 1. Overview of AWS Load Balancers

AWS Elastic Load Balancing (ELB) provides managed traffic distribution services.

AWS currently supports:

| Load Balancer Type | Main Purpose                     |
| ------------------ | -------------------------------- |
| ALB                | HTTP/HTTPS application routing   |
| NLB                | High-performance TCP/UDP routing |
| GWLB               | Security appliance routing       |
| CLB                | Legacy AWS Load Balancer         |

---

# OSI Layer Understanding

Understanding Load Balancers requires basic OSI layer knowledge.

---

# Layer 4 — Transport Layer

Handles:

* TCP
* UDP
* network connections

Layer 4 Load Balancers:

* route traffic based on IP and ports

---

# Layer 7 — Application Layer

Handles:

* HTTP
* HTTPS
* application-level requests

Layer 7 Load Balancers:

* understand URLs
* hostnames
* headers
* request paths

---

# AWS Load Balancer Layer Mapping

| Load Balancer | OSI Layer         |
| ------------- | ----------------- |
| ALB           | Layer 7           |
| NLB           | Layer 4           |
| GWLB          | Layer 3/4         |
| CLB           | Layer 4 + Layer 7 |

---

# 2. Application Load Balancer (ALB)

---

# What is an ALB

An Application Load Balancer (ALB) is a Layer 7 Load Balancer designed for:

* HTTP traffic
* HTTPS traffic
* application-aware routing

ALBs understand:

* URLs
* domains
* paths
* headers

---

# Why ALBs Are Important

ALBs enable:

* intelligent traffic routing
* microservices architecture
* modern web applications
* scalable backend routing

---

# ALB Traffic Flow

```text id="f4mrf0"
User
↓
Application Load Balancer
↓
Backend Targets
```

---

# Key Features of ALB

| Feature            | Purpose              |
| ------------------ | -------------------- |
| Layer 7 Routing    | HTTP-aware routing   |
| Host-Based Routing | Domain-based routing |
| Path-Based Routing | URL path routing     |
| Health Checks      | Target monitoring    |
| Target Groups      | Backend organization |
| HTTPS Support      | SSL termination      |

---

# ALB in This Project

The architecture implemented:

* Public ALB
* Internal ALB

---

# Public ALB

Used for:

* internet-facing frontend traffic

Flow:

```text id="grvt6r"
Internet
↓
Public ALB
↓
Web Tier
```

---

# Internal ALB

Used for:

* private backend communication

Flow:

```text id="sljlwm"
Web Tier
↓
Internal ALB
↓
App Tier
```

---

# Why ALB Was Chosen

The project required:

* HTTP routing
* scalable web traffic handling
* health checks
* Multi-AZ traffic distribution
* future routing rule experimentation

ALB was the ideal choice.

---

# Host-Based Routing

ALB can route traffic based on:

* domain names

Example:

```text id="2g8g40"
api.example.com → API Servers
app.example.com → App Servers
```

---

# Path-Based Routing

ALB can route traffic based on:

* URL paths

Example:

```text id="vk8b06"
/api/* → Backend API
/images/* → Image Server
```

---

# Routing Experiments in This Project

The project explored:

* ALB listener rules
* routing conditions
* traffic forwarding logic

using:

* simple test applications

---

# Enterprise Use Cases of ALB

| Use Case             | Explanation           |
| -------------------- | --------------------- |
| Web Applications     | HTTP traffic routing  |
| Microservices        | Path-based routing    |
| APIs                 | REST endpoint routing |
| Multi-Domain Hosting | Host-based routing    |

---

# ALB Advantages

| Advantage           | Explanation                 |
| ------------------- | --------------------------- |
| Intelligent Routing | Application-aware           |
| HTTPS Support       | SSL/TLS termination         |
| Health Checks       | Automatic target validation |
| Scalable            | AWS-managed scaling         |

---

# ALB Limitations

| Limitation                      | Explanation                         |
| ------------------------------- | ----------------------------------- |
| Not Ideal for Ultra-Low Latency | Higher processing overhead          |
| HTTP-Focused                    | Not optimized for raw TCP workloads |

---

# 3. Network Load Balancer (NLB)

---

# What is an NLB

A Network Load Balancer (NLB) is a Layer 4 Load Balancer designed for:

* ultra-high performance
* low latency
* TCP/UDP traffic

NLB routes traffic based on:

* IP addresses
* ports
* TCP/UDP protocols

---

# Why NLB Exists

Some applications require:

* extremely fast connection handling
* millions of requests per second
* minimal latency

ALB processing overhead may be unnecessary for such workloads.

---

# NLB Traffic Flow

```text id="gk7d8o"
Client
↓
NLB
↓
TCP Backend Servers
```

---

# Key Features of NLB

| Feature           | Purpose                  |
| ----------------- | ------------------------ |
| Layer 4 Routing   | TCP/UDP traffic          |
| Ultra Low Latency | Fast packet forwarding   |
| Static IP Support | Fixed IP addresses       |
| High Throughput   | Massive traffic handling |

---

# Real-World Use Cases

| Use Case            | Explanation              |
| ------------------- | ------------------------ |
| Gaming Servers      | Low latency              |
| Streaming Platforms | Fast TCP handling        |
| Financial Systems   | High-performance traffic |
| VoIP Systems        | UDP traffic              |

---

# Difference Between ALB and NLB

| Feature            | ALB             | NLB                         |
| ------------------ | --------------- | --------------------------- |
| OSI Layer          | Layer 7         | Layer 4                     |
| Protocol Awareness | HTTP/HTTPS      | TCP/UDP                     |
| Routing Type       | Path/Host Based | Port/IP Based               |
| Latency            | Higher          | Lower                       |
| Use Cases          | Web Apps        | High-performance networking |

---

# NLB in Enterprise Environments

NLBs are commonly used for:

* high-performance backend systems
* real-time applications
* large-scale TCP services

---

# Was NLB Used in This Project?

No.

The project focused mainly on:

* HTTP applications
* frontend/backend web traffic

Therefore:

* ALB was more suitable.

---

# 4. Gateway Load Balancer (GWLB)

---

# What is GWLB

Gateway Load Balancer (GWLB) is designed for:

* security appliances
* firewall systems
* deep packet inspection
* network security services

---

# Why GWLB Exists

Large enterprises often deploy:

* virtual firewalls
* IDS/IPS systems
* packet inspection appliances

GWLB helps distribute traffic through these systems.

---

# GWLB Architecture

```text id="q0v4p6"
Network Traffic
↓
GWLB
↓
Security Appliances
↓
Application Infrastructure
```

---

# Key Features of GWLB

| Feature                        | Purpose                    |
| ------------------------------ | -------------------------- |
| Security Appliance Integration | Firewall routing           |
| Traffic Inspection             | Deep packet analysis       |
| Transparent Scaling            | Security appliance scaling |

---

# Enterprise Use Cases

| Use Case             | Explanation            |
| -------------------- | ---------------------- |
| Enterprise Firewalls | Centralized inspection |
| Intrusion Detection  | Security monitoring    |
| Network Security     | Packet filtering       |

---

# Was GWLB Used in This Project?

No.

The project focused on:

* application infrastructure
* networking
* routing
* scalability

not:

* advanced network security appliances

---

# 5. Classic Load Balancer (CLB)

---

# What is CLB

Classic Load Balancer (CLB) is AWS’s older generation Load Balancer.

It supports:

* basic Layer 4 and Layer 7 functionality

---

# Why CLB Is Considered Legacy

AWS now recommends:

* ALB
* NLB

because they provide:

* better scalability
* more features
* modern routing capabilities

---

# Limitations of CLB

| Limitation               | Explanation                |
| ------------------------ | -------------------------- |
| Limited Routing Features | No advanced listener rules |
| Older Architecture       | Less flexible              |
| Reduced Modern Support   | ALB/NLB preferred          |

---

# When CLB Might Still Be Used

Legacy applications that:

* were designed before ALB/NLB existed

may still use CLB.

---

# AWS Recommendation

For modern architectures:

* ALB and NLB are preferred.

---

# Load Balancer Comparison

| Feature                     | ALB     | NLB | GWLB        | CLB     |
| --------------------------- | ------- | --- | ----------- | ------- |
| OSI Layer                   | 7       | 4   | 3/4         | 4/7     |
| HTTP Awareness              | Yes     | No  | No          | Limited |
| TCP/UDP Support             | Limited | Yes | Yes         | Yes     |
| Host-Based Routing          | Yes     | No  | No          | No      |
| Path-Based Routing          | Yes     | No  | No          | No      |
| Security Appliance Support  | No      | No  | Yes         | No      |
| Recommended for Modern Apps | Yes     | Yes | Specialized | No      |

---

# Load Balancer Selection Strategy

---

# Use ALB When

* building web applications
* using HTTP/HTTPS
* requiring intelligent routing
* deploying microservices

---

# Use NLB When

* ultra-low latency is required
* handling TCP/UDP workloads
* supporting high-performance applications

---

# Use GWLB When

* integrating security appliances
* inspecting network traffic
* deploying enterprise firewalls

---

# Avoid CLB for New Architectures

Use:

* ALB
* NLB

instead.

---

# Load Balancer Architecture Used in This Project

---

# Public ALB

```text id="tjlwmx"
Internet
↓
Public ALB
↓
Web Tier
```

---

# Internal ALB

```text id="h5q0m5"
Web Tier
↓
Internal ALB
↓
App Tier
```

---

# Concepts Implemented in This Project

| Concept          | Implementation            |
| ---------------- | ------------------------- |
| ALB              | Frontend traffic routing  |
| Internal ALB     | Backend traffic isolation |
| Health Checks    | Target monitoring         |
| Listener Rules   | Routing experimentation   |
| Multi-AZ Routing | HA traffic distribution   |

---

# Summary

AWS provides multiple Load Balancer types optimized for different workloads.

This chapter explained:

* ALB
* NLB
* GWLB
* CLB
* Layer 4 vs Layer 7 routing
* enterprise Load Balancer selection

The project primarily implemented:

* Application Load Balancers

because the architecture focused on:

* web traffic
* scalable frontend/backend routing
* high availability
* intelligent HTTP traffic management


* internal ALB architecture
* enterprise traffic engineering


# Chapter 3 — Application Load Balancer Deep Dive

Application Load Balancer (ALB) is one of the most important AWS services for modern web architectures.

ALB operates at:

# Layer 7 (Application Layer)

which means it understands:

* HTTP requests
* URLs
* headers
* hostnames
* query strings
* routing conditions

This makes ALB highly suitable for:

* web applications
* APIs
* microservices
* scalable frontend/backend architectures

The project extensively used:

* Public ALB
* Internal ALB
* listener rules
* routing conditions
* target groups
* health checks

to build a production-style multi-tier architecture.

---

# 1. Layer 7 Routing

---

# What is Layer 7 Routing

Layer 7 routing means:

* traffic decisions are made using application-level information.

Unlike Layer 4 Load Balancers:

* ALB can inspect HTTP requests deeply.

---

# ALB Can Inspect

| HTTP Component | Example         |
| -------------- | --------------- |
| Host Header    | app.example.com |
| URL Path       | /api/users      |
| Query String   | ?env=prod       |
| HTTP Headers   | User-Agent      |
| HTTP Method    | GET / POST      |

---

# Layer 7 Routing Flow

```text id="e7xj92"
User Request
↓
ALB Inspects HTTP Request
↓
Routing Decision
↓
Target Group
```

---

# Why Layer 7 Routing Is Powerful

Benefits:

* intelligent routing
* microservices support
* API segmentation
* multi-domain hosting
* advanced traffic engineering

---

# Example

```text id="2upm8z"
example.com/api/*
↓
API Servers

example.com/images/*
↓
Image Servers
```

ALB routes traffic based on:

* URL path

---

# Layer 7 Routing in This Project

The project explored:

* host-based routing
* path-based routing
* listener conditions
* traffic forwarding

using:

* ALB listener rules

---

# 2. HTTP Request Inspection

---

# What is HTTP Request Inspection

ALB analyzes incoming HTTP requests before forwarding traffic.

This includes inspecting:

* headers
* paths
* domains
* query strings
* methods

---

# Request Inspection Flow

```text id="iw4u0s"
HTTP Request
↓
ALB Inspection Engine
↓
Rule Matching
↓
Target Group Forwarding
```

---

# Why Request Inspection Matters

It enables:

* intelligent traffic routing
* advanced application architectures
* service separation
* flexible backend design

---

# Example Request

```text id="0zjlwm"
GET /api/users HTTP/1.1
Host: api.b4n3xus.in
```

ALB can evaluate:

* path
* hostname
* headers

before forwarding traffic.

---

# Real-World Use Cases

| Use Case            | Example          |
| ------------------- | ---------------- |
| API Routing         | /api/*           |
| Static Content      | /images/*        |
| Multi-Domain Apps   | app.example.com  |
| Environment Routing | dev/prod traffic |

---

# 3. Listener Concepts

---

# What is a Listener

A Listener checks for incoming traffic on:

* a specific port
* a specific protocol

Example:

```text id="jlwm93"
HTTP : 80
HTTPS : 443
```

---

# Listener Workflow

```text id="jj4m0s"
User Request
↓
Listener
↓
Rule Evaluation
↓
Target Group
```

---

# Listener Components

| Component      | Purpose             |
| -------------- | ------------------- |
| Protocol       | HTTP / HTTPS        |
| Port           | Traffic entry point |
| Rules          | Routing logic       |
| Default Action | Fallback routing    |

---

# Listener Used in This Project

The ALB used:

* HTTP Listener on Port 80

for:

* frontend traffic handling
* routing experiments
* backend forwarding

---

# Multiple Listeners

An ALB can have:

* multiple listeners

Example:

| Port | Purpose |
| ---- | ------- |
| 80   | HTTP    |
| 443  | HTTPS   |

---

# HTTPS Listeners

HTTPS listeners support:

* SSL/TLS encryption
* secure communication
* certificate integration

---

# 4. Rules and Priorities

---

# What are Listener Rules

Listener rules define:

* how traffic should be routed

based on:

* conditions
* priorities

---

# Rule Evaluation Flow

```text id="2o5z0o"
Request
↓
Listener
↓
Rule Evaluation
↓
Matched Rule
↓
Target Group
```

---

# Why Priorities Matter

ALB evaluates rules:

* from lowest priority number
* to highest priority number

First matching rule wins.

---

# Example

| Priority | Condition         | Action   |
| -------- | ----------------- | -------- |
| 1        | /api/*            | API TG   |
| 2        | /images/*         | Image TG |
| Default  | All Other Traffic | Web TG   |

---

# Practical Example

Suppose request:

```text id="4o8dyx"
/api/users
```

ALB:

* checks Rule 1
* matches `/api/*`
* forwards traffic to API Target Group

---

# Rule Priority Importance

Incorrect priority configuration may:

* route traffic incorrectly
* bypass intended services
* create unexpected behavior

---

# Rule Priorities in This Project

The project experimented with:

* custom listener rules
* priority ordering
* multiple forwarding conditions

to understand:

* ALB traffic flow logic

---

# 5. Default Actions

---

# What is a Default Action

A Default Action defines:

* what ALB should do
* when no listener rule matches

---

# Default Action Flow

```text id="o7lm31"
Request
↓
No Matching Rule
↓
Default Action Executed
```

---

# Common Default Actions

| Action         | Purpose                |
| -------------- | ---------------------- |
| Forward        | Send to target group   |
| Redirect       | Redirect traffic       |
| Fixed Response | Return custom response |

---

# Example

```text id="n7q6mx"
No Rule Match
↓
Forward to Default Web Target Group
```

---

# Default Action in This Project

The ALB default action:

* forwarded unmatched traffic
* to the primary frontend target group

---

# Why Default Actions Are Important

Without default actions:

* unmatched traffic would fail

Default actions ensure:

* traffic continuity
* fallback handling

---

# 6. Target Groups

---

# What is a Target Group

A Target Group is a collection of backend resources that receive traffic from the ALB.

Targets can include:

* EC2 instances
* IP addresses
* containers

---

# ALB Target Flow

```text id="63jlwm"
ALB
↓
Target Group
↓
Backend Servers
```

---

# Why Target Groups Matter

Target Groups provide:

* backend organization
* traffic separation
* health monitoring
* scalable routing

---

# Target Groups in This Project

The architecture used:

* Web Tier Target Group
* App Tier Target Group

---

# Public ALB Flow

```text id="zvmx9j"
Public ALB
↓
Web Target Group
↓
Web EC2 Instances
```

---

# Internal ALB Flow

```text id="3o0fg5"
Internal ALB
↓
App Target Group
↓
Backend EC2 Instances
```

---

# Target Types

| Target Type | Example            |
| ----------- | ------------------ |
| Instance    | EC2                |
| IP          | Custom IP targets  |
| Lambda      | Serverless targets |

---

# Benefits of Target Groups

| Benefit              | Explanation               |
| -------------------- | ------------------------- |
| Traffic Organization | Separate workloads        |
| Scalability          | Easy backend expansion    |
| Health Monitoring    | Target validation         |
| Routing Flexibility  | Multiple backend services |

---

# 7. Health Checks

---

# What are ALB Health Checks

Health checks verify:

* whether backend targets are healthy

before sending traffic.

---

# Why Health Checks Are Important

Without health checks:

* traffic may route to failed servers

causing:

* downtime
* failed requests
* poor user experience

---

# Health Check Workflow

```text id="0yzj6d"
ALB
↓
Health Check Request
↓
Target Response
↓
Healthy / Unhealthy
```

---

# Health Check Components

| Component | Purpose             |
| --------- | ------------------- |
| Protocol  | HTTP/HTTPS          |
| Path      | Endpoint to monitor |
| Interval  | Check frequency     |
| Timeout   | Response wait time  |
| Threshold | Failure tolerance   |

---

# Example Health Check

```text id="9mjlwm"
HTTP GET /
Port 80
```

---

# Health Checks in This Project

The project configured:

* HTTP health checks
* frontend monitoring
* backend monitoring

for:

* automatic target validation

---

# Automatic Failure Handling

If a server failed:

* ALB marked it unhealthy
* traffic stopped routing to it

---

# Enterprise Importance of Health Checks

Health checks improve:

* high availability
* fault tolerance
* automated recovery
* traffic reliability

---

# ALB Architecture Used in This Project

```text id="c7c7l1"
Internet
↓
Public ALB
↓
Web Tier
↓
Internal ALB
↓
App Tier
```

---

# Practical Concepts Explored

| Concept         | Implementation          |
| --------------- | ----------------------- |
| Listener Rules  | Traffic experiments     |
| Rule Priorities | Request evaluation      |
| Target Groups   | Backend organization    |
| Health Checks   | Failure monitoring      |
| Internal ALB    | Private traffic routing |
| Layer 7 Routing | HTTP-aware forwarding   |

---

# Chapter 4 — ALB Routing Rules & Conditions

One of the most powerful features of Application Load Balancer (ALB) is:

# intelligent request routing

ALB can route traffic dynamically using:

* domains
* URL paths
* headers
* query strings
* source IPs

This enables:

* microservices architecture
* multi-domain hosting
* environment separation
* API routing
* advanced traffic engineering

This chapter explains:

* host-based routing
* path-based routing
* listener conditions
* rule priorities
* header-based routing
* query-string routing
* source IP conditions
* practical routing experiments performed in this project

---

# 1. Host-Based Routing

---

# What is Host-Based Routing

Host-based routing forwards traffic based on:

* domain names
* host headers

---

# Example

```text id="o9z4q1"
api.b4n3xus.in
↓
API Servers

app.b4n3xus.in
↓
Frontend Servers
```

---

# How ALB Identifies Hosts

ALB inspects:

```text id="mjlwm0"
Host Header
```

inside the HTTP request.

---

# Host-Based Routing Flow

```text id="l6c5d2"
Request
↓
Host Header Inspection
↓
Matching Rule
↓
Target Group
```

---

# Why Host-Based Routing Is Useful

Benefits:

* multi-domain hosting
* service separation
* efficient infrastructure usage
* centralized routing

---

# Practical Learning Performed

The project implemented:

* subdomain creation using Route 53
* ALB host-based listener rules
* traffic forwarding experiments

using:

```text id="4v6xj2"
b4n3xus.in
```

---

# Subdomains Used

Examples:

```text id="z2kq8m"
api.b4n3xus.in
test.b4n3xus.in
```

---

# Route 53 Integration

Host-based routing worked together with:

* Route 53 DNS records
* ALB listener rules
* Target Groups

---

# 2. Path-Based Routing

---

# What is Path-Based Routing

Path-based routing forwards traffic based on:

* URL paths

---

# Example

```text id="bxm49r"
/api/*
↓
API Servers

/admin/*
↓
Admin Servers
```

---

# Path Routing Flow

```text id="w2o5p8"
Request URL
↓
ALB Path Inspection
↓
Matching Rule
↓
Target Group
```

---

# Why Path-Based Routing Is Important

Benefits:

* microservices architecture
* API segmentation
* frontend/backend separation
* centralized traffic management

---

# Practical Learning Performed

The project implemented:

* path-based listener rules
* URL-based forwarding
* traffic analysis experiments

using:

* simple web applications

---

# Example Paths Tested

```text id="5rjlwm"
/api/*
/test/*
/admin/*
```

---

# 3. Listener Conditions

---

# What are Listener Conditions

Listener conditions define:

* when a rule should match

ALB evaluates:

* request properties
* matching conditions

before forwarding traffic.

---

# Common ALB Conditions

| Condition Type | Example           |
| -------------- | ----------------- |
| Host Header    | api.example.com   |
| Path Pattern   | /api/*            |
| Header Match   | User-Agent        |
| Query String   | env=prod          |
| Source IP      | Trusted IP ranges |

---

# Listener Condition Flow

```text id="kmq2d1"
Incoming Request
↓
Condition Evaluation
↓
Matching Rule
↓
Traffic Forwarding
```

---

# Why Conditions Are Powerful

Conditions enable:

* intelligent routing
* advanced application architecture
* environment-based traffic control

---

# 4. Rule Priority Evaluation

---

# How Rule Priorities Work

ALB evaluates rules:

* from lowest priority number
* to highest priority number

First match wins.

---

# Example

| Priority | Condition         | Action   |
| -------- | ----------------- | -------- |
| 1        | /api/*            | API TG   |
| 2        | /admin/*          | Admin TG |
| Default  | All Other Traffic | Web TG   |

---

# Request Example

Request:

```text id="mxo93s"
/api/users
```

ALB:

* checks Priority 1
* rule matches
* forwards traffic to API Target Group

---

# Why Priorities Matter

Incorrect priorities may:

* override rules
* misroute traffic
* create unexpected behavior

---

# Practical Experiments Performed

The project tested:

* multiple listener rules
* rule ordering
* priority conflicts
* traffic behavior analysis

---

# 5. Header-Based Routing

---

# What is Header-Based Routing

ALB can route traffic using:

* HTTP headers

---

# Example

```text id="0wjlwm"
User-Agent: Mobile
↓
Mobile Backend

User-Agent: Desktop
↓
Desktop Backend
```

---

# Why Header Routing Is Useful

Use cases:

* mobile optimization
* API versioning
* environment testing
* custom client handling

---

# Enterprise Use Cases

| Use Case       | Example                 |
| -------------- | ----------------------- |
| Mobile Apps    | Mobile-specific backend |
| API Versioning | v1 vs v2 APIs           |
| A/B Testing    | Experimental traffic    |

---

# 6. Query-String Routing

---

# What is Query-String Routing

ALB can inspect:

* URL query parameters

before routing traffic.

---

# Example

```text id="k9y4v7"
example.com?env=prod
↓
Production Backend

example.com?env=dev
↓
Development Backend
```

---

# Query Routing Flow

```text id="3v0nqw"
HTTP Request
↓
Query String Inspection
↓
Matching Rule
↓
Target Group
```

---

# Enterprise Use Cases

| Use Case                 | Example         |
| ------------------------ | --------------- |
| Environment Separation   | prod/dev        |
| Feature Testing          | beta features   |
| API Traffic Segmentation | version routing |

---

# 7. Source IP Conditions

---

# What are Source IP Conditions

ALB can route traffic based on:

* client source IP address

---

# Example

```text id="5jlwmq"
Corporate Office IP
↓
Internal Application

Public IP
↓
Public Application
```

---

# Why Source IP Routing Is Useful

Benefits:

* regional routing
* restricted environments
* internal-only applications
* enterprise access control

---

# Enterprise Example

Companies may allow:

* internal applications
* admin dashboards

only from:

* corporate IP ranges

---

# Practical Learning Performed

The project explored:

* ALB listener conditions
* routing logic
* traffic forwarding analysis
* multiple routing strategies

to understand:

* enterprise traffic engineering concepts

---

# Practical Learning Performed

---

# Listener Rule Experimentation

Implemented:

* custom listener rules
* multiple condition combinations
* routing priority testing

---

# Host-Based Routing Implementation

Configured:

* Route 53 subdomains
* ALB host conditions
* target forwarding

---

# Path-Based Routing Implementation

Implemented:

* URL path conditions
* backend traffic forwarding
* path-specific target groups

---

# Traffic Forwarding Analysis

Analyzed:

* request routing behavior
* ALB rule evaluation
* health-based forwarding
* backend communication flow

---

# Architecture Used for Routing Experiments

```text id="y2v9vm"
User
↓
Public ALB
↓
Listener Rules
↓
Target Groups
↓
Backend Targets
```
# Chapter 5 — Reverse Proxy Concepts

Modern enterprise applications commonly separate:

* frontend services
* backend APIs
* internal application logic

Instead of exposing backend servers directly to users, organizations use:

# Reverse Proxies

A reverse proxy sits between:

* clients
* backend services

and intelligently forwards requests.

This architecture improves:

* security
* scalability
* backend abstraction
* traffic control
* application organization

This chapter explains:

* reverse proxy fundamentals
* Nginx reverse proxy architecture
* API forwarding
* backend abstraction
* request routing
* frontend/backend separation
* practical implementation from this project

---

# 1. What is a Reverse Proxy

---

# Definition

A Reverse Proxy is a server that receives client requests and forwards them to backend servers on behalf of the client.

Instead of users communicating directly with backend services:

* requests first reach the reverse proxy.

---

# Basic Reverse Proxy Flow

```text id="n9x3m2"
Client
↓
Reverse Proxy
↓
Backend Server
```

---

# Why Reverse Proxies Are Important

Reverse proxies provide:

* backend hiding
* traffic routing
* centralized request handling
* security improvements
* scalability support

---

# Difference Between Forward Proxy and Reverse Proxy

| Type          | Purpose                  |
| ------------- | ------------------------ |
| Forward Proxy | Protects clients         |
| Reverse Proxy | Protects backend servers |

---

# Real-World Analogy

Imagine a restaurant.

Customers:

* do not directly enter the kitchen

Instead:

* waiters receive requests
* communicate with kitchen staff
* return responses

The reverse proxy acts like:

* the waiter

between:

* users
* backend systems

---

# Reverse Proxy in This Project

The project implemented:

* Nginx reverse proxy architecture

to:

* separate frontend and backend services
* forward API traffic
* isolate backend infrastructure

---

# 2. Nginx Reverse Proxy Architecture

---

# What is Nginx

Nginx is a high-performance:

* web server
* reverse proxy
* load balancer

widely used in enterprise architectures.

---

# Why Nginx Was Used

The project used Nginx because it provides:

* reverse proxy capabilities
* API forwarding
* traffic routing
* frontend hosting
* efficient request handling

---

# Nginx Architecture in This Project

```text id="7tq4l1"
User
↓
Nginx
↓
Internal ALB
↓
Application Tier
```

---

# Frontend and Backend Separation

The architecture separated:

* React frontend
* Node.js backend

using:

* Nginx reverse proxy routing

---

# Request Handling Flow

```text id="m4vw91"
Frontend Request
↓
Nginx
↓
Static Frontend Content
```

```text id="2njlwm"
API Request
↓
Nginx
↓
Internal ALB
↓
Backend APIs
```

---

# Why This Architecture Is Important

Benefits:

* cleaner architecture
* centralized request handling
* backend protection
* easier scaling
* simplified frontend deployment

---

# Enterprise Use Cases of Nginx

| Use Case        | Explanation          |
| --------------- | -------------------- |
| Reverse Proxy   | Backend abstraction  |
| Static Hosting  | Frontend delivery    |
| API Gateway     | Request forwarding   |
| SSL Termination | HTTPS handling       |
| Load Balancing  | Traffic distribution |

---

# 3. API Forwarding

---

# What is API Forwarding

API forwarding means:

* requests received by Nginx
* are forwarded to backend API services

---

# API Forwarding Flow

```text id="b7r4c8"
/api/*
↓
Nginx Reverse Proxy
↓
Internal ALB
↓
Backend APIs
```

---

# Why API Forwarding Is Important

Benefits:

* backend abstraction
* centralized routing
* API protection
* cleaner frontend integration

---

# API Routing in This Project

The project implemented:

```text
/api/*
↓
Internal ALB
↓
Application Tier
```

---

# Example User Request

```text id="t6wz2f"
https://b4n3xus.in/api/users
```

Nginx:

* intercepted the request
* forwarded it internally
* backend processed the API

---

# Why Backend APIs Were Not Public

Direct backend exposure increases:

* security risks
* attack surface
* unauthorized access possibilities

Instead:

* Nginx handled public requests
* backend remained private

---

# Enterprise API Architecture

Modern applications commonly use:

* API gateways
* reverse proxies
* internal routing layers

similar to this architecture.

---

# 4. Backend Abstraction

---

# What is Backend Abstraction

Backend abstraction means:

* users do not directly see backend infrastructure

The reverse proxy hides:

* internal servers
* backend IPs
* service architecture

---

# Backend Abstraction Flow

```text id="4u3mzw"
User
↓
Nginx
↓
Internal Backend Services
```

---

# Why Backend Abstraction Is Important

Benefits:

* improved security
* infrastructure flexibility
* easier scaling
* internal architecture hiding

---

# Example

Users access:

```text id="n3jlwm"
https://b4n3xus.in
```

They do NOT see:

* private backend IPs
* internal ALB
* application server details

---

# Enterprise Advantages

| Benefit     | Explanation                 |
| ----------- | --------------------------- |
| Security    | Backend hidden              |
| Flexibility | Backend changes transparent |
| Scalability | Easy backend expansion      |
| Simplicity  | Clean frontend URLs         |

---

# Backend Abstraction in This Project

The architecture hid:

* backend EC2 instances
* internal ALB
* private application services

behind:

* Nginx reverse proxy

---

# 5. Request Routing

---

# What is Request Routing

Request routing means:

* directing incoming traffic
* to appropriate backend services

based on:

* paths
* request type
* application logic

---

# Routing Flow

```text id="y7v3nm"
Incoming Request
↓
Nginx Evaluation
↓
Routing Decision
↓
Backend Target
```

---

# Routing Logic Used in This Project

| Request Type | Destination  |
| ------------ | ------------ |
| /            | Frontend     |
| /api/*       | Backend APIs |

---

# Frontend Request Example

```text id="rjlwm0"
/
↓
React Frontend
```

---

# API Request Example

```text id="c0q7w2"
/api/users
↓
Internal ALB
↓
App Tier
```

---

# Why Request Routing Matters

Request routing improves:

* application organization
* scalability
* traffic management
* frontend/backend separation

---

# Enterprise Request Routing

Modern cloud applications commonly use:

* reverse proxies
* API gateways
* intelligent traffic routing

to manage:

* multiple services
* APIs
* microservices

---

# 6. Frontend/Backend Separation

---

# What is Frontend/Backend Separation

Frontend/backend separation means:

* UI layer
* backend logic layer

operate independently.

---

# Architecture Separation

```text id="r9t0cw"
Frontend Layer
↓
Reverse Proxy
↓
Backend API Layer
```

---

# Frontend in This Project

The frontend used:

* React application

served through:

* Nginx

---

# Backend in This Project

The backend used:

* Node.js application
* PM2 process management

hosted in:

* private application tier

---

# Why Separation Is Important

Benefits:

* independent scaling
* cleaner architecture
* easier deployments
* backend security
* modular development

---

# Enterprise Architecture Pattern

Most enterprise systems separate:

* UI services
* APIs
* databases

into:

* isolated layers

---

# Practical Architecture Used

```text id="q5jlwm"
User
↓
Public ALB
↓
Nginx Web Tier
↓
Internal ALB
↓
Node.js App Tier
↓
MySQL Database
```

---

# Nginx Concepts Implemented in This Project

| Concept            | Implementation        |
| ------------------ | --------------------- |
| Reverse Proxy      | Nginx                 |
| API Forwarding     | /api/* routing        |
| Backend Isolation  | Internal ALB          |
| Frontend Hosting   | React frontend        |
| Backend Separation | Private App Tier      |
| Request Routing    | Path-based forwarding |

---

# Chapter 6 — Internal Load Balancer Architecture

Enterprise applications often contain:

* internal APIs
* backend microservices
* application layers
* private communication systems

These services should:

* communicate internally
* remain inaccessible from the public internet

AWS solves this using:

# Internal Load Balancers

Internal Load Balancers support:

* east-west traffic
* private service communication
* backend routing
* workload isolation

This chapter explains:

* Internal ALB concepts
* east-west traffic management
* internal service communication
* private backend routing
* backend service isolation
* implementation from this project

---

# 1. Internal ALB Concepts

---

# What is an Internal ALB

An Internal Application Load Balancer is an ALB that:

* operates only inside the VPC
* does NOT receive public internet traffic

It is used for:

* internal communication
* backend service routing
* private application architectures

---

# Internal ALB Architecture

```text id="l0q9x4"
Web Tier
↓
Internal ALB
↓
App Tier
```

---

# Difference Between Public and Internal ALB

| Feature               | Public ALB       | Internal ALB     |
| --------------------- | ---------------- | ---------------- |
| Internet Accessible   | Yes              | No               |
| Public IP             | Yes              | No               |
| Backend Communication | Possible         | Primary Purpose  |
| Use Case              | Frontend traffic | Internal routing |

---

# Why Internal ALBs Are Important

Benefits:

* backend isolation
* secure internal communication
* traffic segmentation
* scalable service architecture

---

# Internal ALB in This Project

The architecture implemented:

* Internal ALB between Web Tier and App Tier

This enabled:

* secure API forwarding
* private backend routing
* backend isolation

---

# 2. East-West Traffic Management

---

# What is East-West Traffic

East-west traffic refers to:

* internal communication between services

inside the infrastructure.

---

# East-West Traffic Example

```text id="0mjlwm"
Web Tier
↓
App Tier
↓
Database Tier
```

This communication happens:

* internally inside the VPC

---

# Difference Between North-South and East-West Traffic

| Traffic Type | Meaning                        |
| ------------ | ------------------------------ |
| North-South  | Internet ↔ Application         |
| East-West    | Internal service communication |

---

# Why East-West Traffic Matters

Modern applications contain:

* APIs
* microservices
* backend services

that communicate internally.

---

# East-West Traffic in This Project

The project used:

* Internal ALB
* private routing
* Security Groups

to manage:

* secure backend communication

---

# East-West Flow in This Project

```text id="u8wq1d"
Public ALB
↓
Web Tier
↓
Internal ALB
↓
Private App Tier
```

---

# 3. Internal Service Communication

---

# What is Internal Service Communication

Internal service communication means:

* backend services communicate privately

without exposing traffic publicly.

---

# Why Internal Communication Is Important

Benefits:

* stronger security
* reduced exposure
* backend protection
* cleaner architecture

---

# Internal Communication Flow

```text id="m4jlwm"
Frontend
↓
Internal ALB
↓
Backend API
```

---

# Internal Communication in This Project

The architecture implemented:

* Web Tier to App Tier communication
* private backend API routing
* internal ALB forwarding

---

# Security Advantages

The backend services:

* had no direct public access

Traffic passed through:

* Internal ALB
* Security Groups
* private subnets

---

# Enterprise Architecture Pattern

Most enterprise applications:

* isolate backend services
* avoid public backend exposure
* use internal traffic routing layers

---

# 4. Private Backend Routing

---

# What is Private Backend Routing

Private backend routing means:

* traffic is forwarded internally
* using private networking

instead of:

* public internet routing

---

# Private Routing Flow

```text id="2v7p6m"
Nginx
↓
Internal ALB
↓
Private App Tier
```

---

# Why Private Routing Is Important

Benefits:

* backend protection
* reduced attack surface
* secure communication
* internal traffic control

---

# Private Routing in This Project

The architecture used:

* private subnets
* Internal ALB
* Security Groups

to ensure:

* backend APIs remained private

---

# Backend Routing Strategy

| Layer         | Accessibility   |
| ------------- | --------------- |
| Public ALB    | Internet-facing |
| Web Tier      | Public subnet   |
| Internal ALB  | Private         |
| App Tier      | Private         |
| Database Tier | Private         |

---

# Enterprise Security Benefits

Private backend routing:

* prevents direct exposure
* isolates backend services
* supports zero-trust architecture

---

# 5. Backend Service Isolation

---

# What is Backend Isolation

Backend isolation means:

* internal application services remain separated
* from direct user access

---

# Why Backend Isolation Matters

Backend services commonly contain:

* APIs
* authentication logic
* business logic
* database communication

Direct exposure increases:

* attack surface
* security risks

---

# Isolation Architecture

```text id="j9w3q7"
User
↓
Public Layer
↓
Internal Routing Layer
↓
Backend Services
```

---

# Backend Isolation in This Project

The architecture isolated:

* Node.js backend services
* database communication

inside:

* private subnets

---

# Security Layers Used

| Security Layer  | Purpose                |
| --------------- | ---------------------- |
| Internal ALB    | Private routing        |
| Security Groups | Traffic restriction    |
| Private Subnets | Isolation              |
| NAT Gateway     | Secure outbound access |

---

# Enterprise Benefits of Backend Isolation

| Benefit         | Explanation                 |
| --------------- | --------------------------- |
| Security        | Reduced exposure            |
| Traffic Control | Internal-only access        |
| Scalability     | Independent backend scaling |
| Fault Isolation | Service separation          |

---

# Practical Architecture Used in This Project

```text id="c6xq9m"
Internet
↓
Public ALB
↓
Web Tier
↓
Internal ALB
↓
Private App Tier
↓
Database Tier
```

---

# Concepts Implemented in This Project

| Concept             | Implementation               |
| ------------------- | ---------------------------- |
| Reverse Proxy       | Nginx                        |
| Internal ALB        | Private backend routing      |
| East-West Traffic   | Internal communication       |
| Backend Isolation   | Private subnets              |
| API Forwarding      | /api/* routing               |
| Frontend Separation | React + Node.js architecture |

# Chapter 7 — High Availability

Modern enterprise applications must remain operational even during:

* server failures
* infrastructure issues
* traffic spikes
* Availability Zone outages

Downtime affects:

* users
* business operations
* reliability
* revenue
* customer trust

To solve this, enterprise cloud architectures implement:

# High Availability (HA)

High Availability ensures:

* applications remain accessible
* downtime is minimized
* traffic continues flowing
* failures do not stop services completely

This chapter explains:

* High Availability fundamentals
* fault tolerance
* Multi-AZ architecture
* redundancy
* self-healing systems
* enterprise HA strategies
* HA implementation from this project

---

# 1. What is High Availability

---

# Definition

High Availability (HA) is the design principle of ensuring systems remain operational with minimal downtime.

HA architectures are designed to:

* continue functioning during failures
* reduce service interruptions
* maximize uptime

---

# Simple Explanation

Instead of depending on:

* one server
* one network path
* one Availability Zone

HA architectures use:

* multiple redundant components

so that:

* failure of one component does not stop the application.

---

# Basic HA Architecture

```text id="p4z8mw"
Users
↓
Load Balancer
↓
Multiple Servers
```

---

# Why HA Is Important

Without HA:

* single failures cause downtime

Enterprise systems must avoid:

# Single Points of Failure (SPOF)

---

# Real-World Analogy

Imagine a hospital power system.

Hospitals use:

* backup generators
* multiple power lines
* redundant systems

so operations continue even during failures.

HA works similarly in cloud infrastructure.

---

# High Availability in This Project

The architecture implemented:

* Multi-AZ deployment
* multiple web instances
* multiple app instances
* Load Balancers
* Auto Scaling preparation
* health checks

---

# HA Architecture Used

```text id="7q3d9v"
Public ALB
↓
Web Tier (AZ-1 + AZ-2)
↓
Internal ALB
↓
App Tier (AZ-1 + AZ-2)
```

---

# 2. Fault Tolerance

---

# What is Fault Tolerance

Fault tolerance means:

* systems continue operating
* even when failures occur

---

# Difference Between HA and Fault Tolerance

| Concept           | Meaning                            |
| ----------------- | ---------------------------------- |
| High Availability | Minimize downtime                  |
| Fault Tolerance   | Continue operating during failures |

---

# Fault Tolerance Example

Suppose:

* one web server crashes

The Load Balancer:

* detects failure
* removes unhealthy target
* forwards traffic to healthy instances

Users continue accessing the application.

---

# Fault Tolerance Flow

```text id="m6v2q1"
Server Failure
↓
Health Check Failure
↓
ALB Removes Target
↓
Traffic Routed Elsewhere
```

---

# Why Fault Tolerance Matters

Without fault tolerance:

* single server failure causes outage

Enterprise architectures therefore implement:

* redundancy
* health checks
* multiple instances
* failover systems

---

# Fault Tolerance in This Project

Implemented using:

* ALB health checks
* multiple EC2 instances
* Multi-AZ deployment
* Auto Scaling architecture

---

# Enterprise Fault Tolerance Examples

| Industry   | Requirement                    |
| ---------- | ------------------------------ |
| Banking    | Continuous transaction systems |
| Healthcare | Critical application uptime    |
| E-commerce | Sales continuity               |
| Streaming  | Continuous content delivery    |

---

# 3. Multi-AZ Architecture

---

# What is Multi-AZ Architecture

Multi-AZ architecture distributes infrastructure across:

* multiple Availability Zones

inside the same AWS region.

---

# Why Multi-AZ Is Important

If one Availability Zone fails:

* applications continue operating from another AZ.

---

# Multi-AZ Architecture Flow

```text id="0pjlwm"
ALB
↓
AZ-1 Instances
AZ-2 Instances
```

---

# Availability Zones Used in This Project

```text id="q8m3w4"
us-east-1a
us-east-1b
```

---

# Multi-AZ Infrastructure Used

| Layer           | AZ Distribution |
| --------------- | --------------- |
| Public Subnets  | 2 AZs           |
| Web Tier        | 2 AZs           |
| App Tier        | 2 AZs           |
| Private Subnets | 2 AZs           |

---

# Why Multi-AZ Improves Availability

Benefits:

* infrastructure redundancy
* failure isolation
* improved uptime
* better resilience

---

# Example Failure Scenario

Suppose:

* us-east-1a experiences issues

The ALB continues routing traffic to:

* healthy targets in us-east-1b

---

# Enterprise Importance of Multi-AZ

Most enterprise cloud architectures use:

* Multi-AZ deployment

as a standard HA strategy.

---

# 4. Redundancy

---

# What is Redundancy

Redundancy means:

* creating duplicate infrastructure components

to avoid dependency on a single resource.

---

# Examples of Redundant Components

| Component      | Redundancy Example     |
| -------------- | ---------------------- |
| Servers        | Multiple EC2 instances |
| AZs            | Multi-AZ deployment    |
| Networking     | Multiple subnets       |
| Load Balancers | Multi-target routing   |

---

# Redundancy Flow

```text id="n4q7dy"
Primary Instance
↓
Failure
↓
Secondary Instance Handles Traffic
```

---

# Why Redundancy Is Important

Without redundancy:

* failures stop services completely

Redundancy improves:

* resilience
* uptime
* reliability

---

# Redundancy in This Project

Implemented using:

* multiple Web Tier instances
* multiple App Tier instances
* Multi-AZ deployment
* Load Balancers

---

# Enterprise Redundancy Strategies

| Strategy            | Purpose                    |
| ------------------- | -------------------------- |
| Multi-AZ Deployment | Zone redundancy            |
| Auto Scaling        | Instance redundancy        |
| Load Balancing      | Traffic redundancy         |
| Health Checks       | Automatic failure handling |

---

# 5. Self-Healing Systems

---

# What are Self-Healing Systems

Self-healing systems automatically:

* detect failures
* recover infrastructure
* replace unhealthy resources

without manual intervention.

---

# Self-Healing Flow

```text id="y9t4v6"
Instance Failure
↓
Health Check Failure
↓
ASG Detects Problem
↓
New Instance Created
```

---

# Why Self-Healing Is Important

Benefits:

* reduced downtime
* automated recovery
* operational efficiency
* reduced manual intervention

---

# Self-Healing Components in AWS

| Service       | Function                   |
| ------------- | -------------------------- |
| ALB           | Detect unhealthy targets   |
| ASG           | Replace failed instances   |
| Health Checks | Monitor application health |

---

# Self-Healing in This Project

The project implemented:

* health checks
* Auto Scaling Groups
* Launch Templates
* AMI-based recovery

---

# Example Scenario

Suppose:

* App Tier instance crashes

The ASG:

* launches replacement instance automatically

The ALB:

* routes traffic only to healthy targets

---

# Enterprise Importance

Self-healing is critical for:

* large-scale infrastructure
* production systems
* cloud-native architectures

---

# 6. Enterprise HA Strategies

---

# Common Enterprise HA Strategies

Enterprise systems combine multiple HA approaches.

---

# Strategy 1 — Multi-AZ Deployment

Distributes workloads across:

* multiple Availability Zones

---

# Strategy 2 — Load Balancing

Distributes traffic across:

* multiple backend servers

---

# Strategy 3 — Auto Scaling

Automatically:

* adds instances
* replaces failed systems

---

# Strategy 4 — Health Monitoring

Continuously checks:

* application health
* instance health
* service availability

---

# Strategy 5 — Redundant Infrastructure

Avoids:

# single points of failure

---

# Enterprise HA Architecture Example

```text id="4rjlwm"
Users
↓
ALB
↓
AZ-1 Web Servers
AZ-2 Web Servers
↓
Internal ALB
↓
AZ-1 App Servers
AZ-2 App Servers
```

---

# HA Strategies Used in This Project

| HA Strategy    | Implementation               |
| -------------- | ---------------------------- |
| Multi-AZ       | us-east-1a + us-east-1b      |
| Load Balancing | Public + Internal ALB        |
| Health Checks  | ALB target monitoring        |
| Redundancy     | Multiple instances           |
| Auto Scaling   | Dynamic scaling architecture |

---

# Enterprise Benefits Achieved

The architecture improved:

* uptime
* scalability
* resilience
* automated recovery
* traffic availability

---

# Chapter 8 — Auto Scaling

Cloud environments must handle:

* changing traffic patterns
* unpredictable workloads
* traffic spikes
* growing user demand

Keeping infrastructure fixed leads to:

* resource wastage
* poor scalability
* performance issues

AWS solves this using:

# Auto Scaling

Auto Scaling dynamically adjusts infrastructure capacity based on:

* traffic
* load
* resource utilization

This chapter explains:

* horizontal scaling
* vertical scaling
* dynamic scaling
* scaling policies
* Auto Scaling Groups
* Launch Templates
* AMI concepts
* practical implementation from this project

---

# 1. Horizontal Scaling

---

# What is Horizontal Scaling

Horizontal scaling means:

* adding more servers

instead of increasing server size.

---

# Horizontal Scaling Flow

```text id="k3q7x1"
Traffic Increase
↓
Add More EC2 Instances
↓
Load Balancer Distributes Traffic
```

---

# Why Horizontal Scaling Is Important

Benefits:

* better scalability
* improved availability
* fault tolerance
* easier expansion

---

# Example

Instead of:

```text id="n7w4dy"
1 Large Server
```

Use:

```text id="x9q5mv"
4 Smaller Servers
```

---

# Horizontal Scaling in This Project

The project implemented:

* Auto Scaling Groups
* multiple Web Tier instances
* multiple App Tier instances

behind:

* ALBs

---

# Enterprise Use Cases

Horizontal scaling is commonly used for:

* web applications
* APIs
* microservices
* cloud-native architectures

---

# 2. Vertical Scaling

---

# What is Vertical Scaling

Vertical scaling means:

* increasing server resources

such as:

* CPU
* RAM
* storage

---

# Vertical Scaling Example

```text id="8jlwmx"
t2.micro
↓
t3.large
```

---

# Advantages of Vertical Scaling

| Advantage             | Explanation             |
| --------------------- | ----------------------- |
| Simpler Architecture  | Fewer servers           |
| Easier Small Upgrades | Quick resource increase |

---

# Limitations of Vertical Scaling

| Limitation           | Explanation                |
| -------------------- | -------------------------- |
| Hardware Limits      | Maximum size exists        |
| Downtime Risk        | Resize may require restart |
| Less Fault Tolerance | Single large server        |

---

# Why Horizontal Scaling Was Preferred

The project focused on:

* scalable cloud-native architecture
* redundancy
* HA
* Load Balancer integration

Therefore:

* horizontal scaling was preferred.

---

# 3. Dynamic Scaling

---

# What is Dynamic Scaling

Dynamic scaling automatically adjusts infrastructure capacity based on:

* system load
* traffic
* performance metrics

---

# Dynamic Scaling Flow

```text id="6wq3m7"
Traffic Spike
↓
CPU Usage Increases
↓
ASG Launches New Instances
```

---

# Why Dynamic Scaling Matters

Benefits:

* automatic scaling
* reduced manual intervention
* cost optimization
* performance stability

---

# Example

During low traffic:

* fewer servers run

During high traffic:

* more servers launch automatically

---

# Enterprise Importance

Dynamic scaling is critical for:

* modern cloud applications
* unpredictable workloads
* elastic infrastructure

---

# 4. Scaling Policies

---

# What are Scaling Policies

Scaling policies define:

* when scaling should occur

based on:

* metrics
* thresholds
* schedules

---

# Common Scaling Metrics

| Metric          | Example           |
| --------------- | ----------------- |
| CPU Utilization | >70%              |
| Memory Usage    | High RAM          |
| Network Traffic | Increased traffic |
| Request Count   | ALB requests      |

---

# Types of Scaling Policies

| Policy Type       | Purpose                |
| ----------------- | ---------------------- |
| Target Tracking   | Maintain metric target |
| Step Scaling      | Scale incrementally    |
| Scheduled Scaling | Time-based scaling     |

---

# Example Policy

```text id="r2w9q4"
If CPU > 70%
↓
Launch Additional Instance
```

---

# Scaling Concepts Explored in This Project

The project focused on:

* Auto Scaling architecture
* Launch Templates
* AMI-based instance creation
* scaling workflow understanding

---

# 5. Auto Scaling Groups (ASG)

---

# What is an Auto Scaling Group

An Auto Scaling Group automatically:

* launches EC2 instances
* terminates EC2 instances
* maintains desired capacity

---

# ASG Workflow

```text id="3p8v0m"
Traffic Increase
↓
ASG Launches Instances
↓
ALB Registers Targets
```

---

# Why ASGs Are Important

Benefits:

* self-healing
* automatic scaling
* HA support
* operational automation

---

# ASG in This Project

The project implemented:

* Web Tier ASG
* scaling-ready architecture

---

# Practical Configuration

| Configuration    | Value |
| ---------------- | ----- |
| Minimum Capacity | 2     |
| Desired Capacity | 2     |
| Maximum Capacity | 4     |

---

# Meaning of These Values

---

## Minimum Capacity — 2

ASG always maintains:

* at least 2 instances

for:

* redundancy
* HA

---

## Desired Capacity — 2

The ASG attempts to maintain:

* 2 running instances normally

---

## Maximum Capacity — 4

During scaling events:

* ASG can increase up to 4 instances

---

# ASG Benefits in This Project

| Benefit           | Explanation                 |
| ----------------- | --------------------------- |
| High Availability | Multiple instances          |
| Self-Healing      | Failed instance replacement |
| Scalability       | Dynamic expansion           |
| Automation        | Reduced manual effort       |

---

# 6. Launch Templates

---

# What is a Launch Template

A Launch Template defines:

* how EC2 instances should be launched

---

# Launch Template Components

| Component       | Purpose        |
| --------------- | -------------- |
| AMI             | Base OS image  |
| Instance Type   | EC2 size       |
| Security Groups | Firewall rules |
| Key Pair        | SSH access     |
| User Data       | Bootstrapping  |

---

# Why Launch Templates Matter

ASGs use Launch Templates to:

* create identical instances automatically

---

# Launch Template Flow

```text id="9xq3v2"
Launch Template
↓
ASG
↓
New EC2 Instance
```

---

# Launch Templates in This Project

Configured using:

* custom AMI
* predefined SGs
* application-ready configuration

---

# 7. AMI Concepts

---

# What is an AMI

AMI stands for:

# Amazon Machine Image

An AMI is a preconfigured template used to launch EC2 instances.

---

# AMI Contains

| Component          | Example           |
| ------------------ | ----------------- |
| Operating System   | Ubuntu            |
| Installed Software | Nginx / Node.js   |
| Configurations     | Application setup |

---

# Why AMIs Are Important

AMIs enable:

* rapid deployment
* infrastructure consistency
* automated scaling

---

# AMI Workflow

```text id="jlwmx8"
Configured EC2 Instance
↓
Create AMI
↓
Launch Multiple Identical Instances
```

---

# AMI Usage in This Project

The project:

* configured application servers
* created custom AMIs
* used Launch Templates
* enabled ASG deployment

---

# Enterprise Importance of AMIs

AMIs support:

* immutable infrastructure
* automated deployment
* rapid recovery
* scalable architectures

---

# Auto Scaling Architecture Used in This Project

```text id="c8m4q7"
Users
↓
ALB
↓
ASG
↓
Multiple Web Instances
```

---

# Concepts Implemented in This Project

| Concept              | Implementation               |
| -------------------- | ---------------------------- |
| Horizontal Scaling   | ASG-based scaling            |
| Multi-AZ Deployment  | Redundant instances          |
| Launch Templates     | Standardized deployment      |
| AMI-Based Scaling    | Automated instance creation  |
| Self-Healing         | ASG recovery                 |
| Dynamic Architecture | Scaling-ready infrastructure |

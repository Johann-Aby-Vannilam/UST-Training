# Volume 4 — DNS & Route 53

---

<img width="1536" height="1024" alt="Volume 4" src="https://github.com/user-attachments/assets/60a0e608-3782-4b15-8865-33f0c9a48219" />


---

# Chapter 1 — Domain Name System (DNS)

Every modern internet application depends on:

# DNS (Domain Name System)

Without DNS, users would need to remember:

* IP addresses
* server locations
* network endpoints

Instead of using human-friendly names like:

```text
b4n3xus.in
```

users would need to remember:

```text
54.210.x.x
```

DNS solves this problem by translating:

* domain names
  into
* IP addresses

This chapter explains:

* DNS fundamentals
* domain resolution
* public DNS architecture
* DNS records
* DNS propagation
* enterprise DNS concepts
* DNS implementation from this project

---

# 1. DNS Fundamentals

---

# What is DNS

DNS stands for:

# Domain Name System

It is the internet’s naming system used to map:

* domain names
  to
* IP addresses

---

# Simple Explanation

Humans prefer:

```text id="k1p8x3"
b4n3xus.in
```

Computers communicate using:

```text id="d4q7w9"
54.x.x.x
```

DNS acts like:

* the internet phonebook

---

# Why DNS Is Important

Without DNS:

* websites would require IP addresses
* services would be difficult to access
* internet usability would become complex

---

# DNS Architecture

```text id="w8v2m1"
User
↓
DNS Resolver
↓
DNS Servers
↓
IP Address Returned
↓
Website Access
```

---

# Real-World Analogy

Imagine using a phone contact list.

Instead of remembering:

* phone numbers

you remember:

* contact names

DNS works similarly:

* domain names map to IP addresses.

---

# DNS in This Project

The project used:

```text id="p6z4v2"
b4n3xus.in
```

with:

* Route 53
* ALB integration
* subdomain routing

---

# 2. Domain Resolution Process

---

# What is Domain Resolution

Domain resolution is the process of converting:

* domain names
  into
* IP addresses

---

# Example

```text id="f9m3q7"
b4n3xus.in
↓
ALB DNS Name
↓
Backend Infrastructure
```

---

# DNS Resolution Flow

```text id="q0w7n5"
Browser
↓
Recursive Resolver
↓
Root DNS Server
↓
TLD Server
↓
Authoritative DNS Server
↓
IP Address Returned
```

---

# Step-by-Step Resolution Process

---

## Step 1 — User Enters Domain

Example:

```text id="t8m5x1"
https://b4n3xus.in
```

---

## Step 2 — Browser Checks Cache

The browser checks:

* local DNS cache

If not found:

* request moves forward

---

## Step 3 — Recursive Resolver Query

The ISP or DNS resolver receives:

* DNS query request

---

## Step 4 — Root DNS Server

The root server identifies:

* which TLD server to contact

Example:

```text id="m1q4y8"
.in
```

---

## Step 5 — TLD Server

The TLD server identifies:

* authoritative DNS server

for:

```text id="g7w2v6"
b4n3xus.in
```

---

## Step 6 — Authoritative DNS Server

The authoritative server returns:

* final DNS record

---

## Step 7 — Browser Receives IP

Browser receives:

* destination IP or ALB DNS target

and connects to the application.

---

# Why DNS Resolution Matters

Understanding DNS resolution helps explain:

* website connectivity
* DNS troubleshooting
* propagation delays
* cloud traffic flow

---

# 3. Public DNS Architecture

---

# What is Public DNS

Public DNS allows:

* internet users worldwide
* to resolve public domain names

---

# Public DNS Flow

```text id="z2m7w4"
Internet User
↓
Public DNS Infrastructure
↓
Domain Resolution
↓
Application Access
```

---

# Public DNS Components

| Component             | Purpose                     |
| --------------------- | --------------------------- |
| Root DNS Servers      | Top-level DNS hierarchy     |
| TLD Servers           | Domain extension management |
| Authoritative Servers | Final DNS records           |
| Recursive Resolvers   | Client DNS queries          |

---

# Public DNS in This Project

The project used:

* public hosted zones
* internet-facing ALB
* public domain routing

---

# Enterprise Importance

Public DNS enables:

* global application access
* internet-facing services
* scalable web hosting

---

# 4. DNS Records

---

# What are DNS Records

DNS records define:

* how domains behave
* where traffic should route

---

# DNS Record Flow

```text id="v9m2q6"
Domain Name
↓
DNS Record
↓
Destination Resource
```

---

# Common DNS Record Types

| Record Type | Purpose            |
| ----------- | ------------------ |
| A           | IPv4 mapping       |
| AAAA        | IPv6 mapping       |
| CNAME       | Domain alias       |
| MX          | Mail routing       |
| TXT         | Verification data  |
| Alias       | AWS-native routing |

---

# DNS Records Used in This Project

The project implemented:

* A records
* CNAME records
* Alias records
* subdomain mappings

---

# Example

```text id="n5q8w2"
b4n3xus.in
↓
ALB
```

---

# Why DNS Records Matter

DNS records control:

* traffic routing
* domain behavior
* service accessibility

---

# 5. DNS Propagation

---

# What is DNS Propagation

DNS propagation is the time required for DNS changes to spread globally across DNS systems.

---

# Why Propagation Happens

DNS systems cache records to:

* improve speed
* reduce lookup load

Caches must update when records change.

---

# DNS Propagation Flow

```text id="u4m1x9"
DNS Record Updated
↓
Global DNS Cache Refresh
↓
Users Receive Updated Record
```

---

# Propagation Time

DNS changes may take:

* minutes
* hours

depending on:

* TTL settings
* resolver caching

---

# What is TTL

TTL means:

# Time To Live

TTL defines:

* how long DNS records remain cached

---

# Example

| TTL          | Meaning   |
| ------------ | --------- |
| 300 seconds  | 5 minutes |
| 3600 seconds | 1 hour    |

---

# DNS Propagation in This Project

During Route 53 configuration:

* DNS records required propagation time
* domain routing updates were tested gradually

---

# Enterprise Importance of Propagation

Understanding propagation is important for:

* migrations
* failover changes
* DNS troubleshooting
* domain cutovers

---

# Chapter 2 — Route 53 Fundamentals

AWS Route 53 is AWS’s managed DNS service used for:

* domain management
* DNS routing
* health-based routing
* scalable DNS infrastructure

Route 53 integrates deeply with:

* ALBs
* CloudFront
* EC2
* S3
* AWS networking services

This chapter explains:

* Route 53 fundamentals
* hosted zones
* public hosted zones
* DNS management
* AWS integration
* Route 53 implementation from this project

---

# 1. What is Route 53

---

# Definition

Amazon Route 53 is AWS’s:

# scalable managed DNS service

used for:

* domain registration
* DNS routing
* traffic management
* domain resolution

---

# Why It Is Called Route 53

The name comes from:

```text id="m9w3q5"
Port 53
```

which is the standard DNS port.

---

# Route 53 Architecture

```text id="t2m6q1"
User
↓
Route 53 DNS
↓
AWS Resources
```

---

# Why Route 53 Is Important

Benefits:

* highly available DNS
* AWS integration
* scalable routing
* low latency
* global DNS infrastructure

---

# Route 53 in This Project

The project used Route 53 for:

* domain management
* ALB DNS routing
* subdomain creation
* Alias records

---

# 2. Hosted Zones

---

# What is a Hosted Zone

A Hosted Zone stores:

* DNS records
  for a domain.

---

# Example

Hosted Zone:

```text id="w1q8x6"
b4n3xus.in
```

contains:

* A records
* Alias records
* subdomain mappings

---

# Hosted Zone Architecture

```text id="f6m4v2"
Domain
↓
Hosted Zone
↓
DNS Records
```

---

# Types of Hosted Zones

| Type                | Purpose                 |
| ------------------- | ----------------------- |
| Public Hosted Zone  | Internet-facing domains |
| Private Hosted Zone | Internal VPC DNS        |

---

# Hosted Zone Used in This Project

The project implemented:

# Public Hosted Zone

for:

```text id="p3m7w1"
b4n3xus.in
```

---

# 3. Public Hosted Zones

---

# What is a Public Hosted Zone

A Public Hosted Zone allows:

* internet users
* to resolve DNS records publicly

---

# Public Hosted Zone Flow

```text id="r8m2x5"
Internet User
↓
Route 53 Public Hosted Zone
↓
ALB / Infrastructure
```

---

# Why Public Hosted Zones Are Important

They enable:

* public website hosting
* internet application access
* public domain routing

---

# Public Hosted Zone in This Project

Configured for:

* internet-facing ALB
* public frontend access
* subdomain routing

---

# 4. DNS Management

---

# What is DNS Management

DNS management involves:

* creating DNS records
* updating routing
* managing domain behavior

---

# DNS Management Tasks Performed

The project included:

* creating records
* testing DNS propagation
* ALB routing integration
* subdomain mapping

---

# DNS Workflow

```text id="x7m4q9"
Domain
↓
Route 53 Records
↓
ALB
↓
Infrastructure
```

---

# Enterprise DNS Management

Organizations commonly manage:

* production domains
* APIs
* mail records
* environment routing

using centralized DNS platforms like Route 53.

---

# 5. Route 53 Integration with AWS Services

---

# Why Route 53 Integration Matters

Route 53 integrates directly with:

* ALB
* CloudFront
* S3
* EC2
* API Gateway

---

# ALB Integration in This Project

The project integrated:

```text id="v2q9w3"
b4n3xus.in
↓
Alias Record
↓
Public ALB
```

---

# Benefits of AWS Integration

| Benefit                        | Explanation            |
| ------------------------------ | ---------------------- |
| Simplified Routing             | Native AWS integration |
| High Availability              | AWS-managed DNS        |
| Dynamic Infrastructure Support | Scalable cloud routing |

---

# AWS Integration Architecture

```text id="c5m8x1"
Route 53
↓
ALB
↓
Web Tier
```

---

# Chapter 3 — DNS Record Types

DNS records define:

* how traffic should route
* where services are located
* how domains behave

Different record types serve different purposes.

This chapter explains:

* A records
* AAAA records
* CNAME records
* Alias records
* MX records
* TXT records
* practical record usage from this project

---

# 1. A Records

---

# What is an A Record

An A Record maps:

* a domain
  to
* an IPv4 address

---

# Example

```text id="x4m2w8"
b4n3xus.in
↓
54.x.x.x
```

---

# Why A Records Matter

A records are the most common DNS records used for:

* websites
* servers
* public applications

---

# A Records in This Project

The project explored:

* A record routing
* ALB DNS integration
* domain mapping

---

# 2. AAAA Records

---

# What is an AAAA Record

AAAA records map:

* domains
  to
* IPv6 addresses

---

# Example

```text id="m7w1q4"
example.com
↓
2001:db8::1
```

---

# Why AAAA Records Exist

The internet is gradually transitioning toward:

# IPv6

because IPv4 addresses are limited.

---

# 3. CNAME Records

---

# What is a CNAME Record

CNAME stands for:

# Canonical Name

A CNAME points:

* one domain
  to
* another domain

---

# Example

```text id="t5m9w2"
api.b4n3xus.in
↓
backend.example.com
```

---

# Why CNAME Records Matter

Benefits:

* easier domain management
* flexible routing
* simplified subdomain handling

---

# CNAME Records in This Project

The project implemented:

* subdomain routing
* ALB DNS mapping
* routing experiments

---

# 4. Alias Records

---

# What is an Alias Record

Alias Records are AWS-specific DNS records that route:

* domains
  directly to:
* AWS resources

---

# Example

```text id="y3m6q8"
b4n3xus.in
↓
Public ALB
```

---

# Why Alias Records Are Important

Alias records support:

* root domains
* AWS-native routing
* scalable infrastructure integration

---

# Alias Records in This Project

The project used:

* Alias records
* Route 53 → ALB integration

for:

```text id="j4m8w1"
b4n3xus.in
```

---

# 5. MX Records

---

# What is an MX Record

MX stands for:

# Mail Exchange

MX records define:

* mail server routing

---

# Example

```text id="v8q2m4"
example.com
↓
Google Mail Server
```

---

# Why MX Records Matter

Used for:

* email delivery
* mail routing
* enterprise email systems

---

# 6. TXT Records

---

# What is a TXT Record

TXT records store:

* text-based DNS information

---

# Common TXT Record Uses

| Use Case            | Purpose              |
| ------------------- | -------------------- |
| Domain Verification | Ownership validation |
| SPF                 | Email security       |
| DKIM                | Mail authentication  |

---

# Enterprise Importance of TXT Records

TXT records help with:

* email security
* verification
* cloud service validation

---

# Record Types Used in This Project

| Record Type | Usage                  |
| ----------- | ---------------------- |
| A Record    | Domain mapping         |
| CNAME       | Subdomain routing      |
| Alias       | ALB integration        |
| TXT         | Validation experiments |

---

# Chapter 4 — Alias vs CNAME

Alias and CNAME records appear similar because both can redirect traffic.

However:

* they behave differently
* support different use cases
* integrate differently with AWS services

Understanding the difference is extremely important for:

* Route 53 configuration
* ALB integration
* enterprise DNS architecture

This chapter explains:

* Alias vs CNAME differences
* AWS-native Alias records
* ALB DNS integration
* enterprise best practices
* implementation from this project

---

# 1. Differences Between Alias and CNAME

---

# What is a CNAME

CNAME points:

* one domain
  to
* another domain

---

# Example

```text id="m5q8x2"
api.b4n3xus.in
↓
backend.example.com
```

---

# What is an Alias Record

Alias records point:

* directly to AWS resources

such as:

* ALB
* CloudFront
* S3

---

# Example

```text id="r2m7w9"
b4n3xus.in
↓
Application Load Balancer
```

---

# Core Difference

| Feature                  | CNAME      | Alias    |
| ------------------------ | ---------- | -------- |
| AWS Native               | No         | Yes      |
| Root Domain Support      | No         | Yes      |
| Works with AWS Resources | Indirectly | Directly |
| Extra DNS Lookup         | Yes        | No       |

---

# Why Root Domain Support Matters

CNAME records cannot be used for:

```text id="x7m1q5"
b4n3xus.in
```

because:

* root domains require A/AAAA-style behavior.

Alias records solve this problem.

---

# 2. AWS-Native Alias Records

---

# Why AWS Created Alias Records

AWS resources:

* scale dynamically
* change IP addresses

Alias records allow Route 53 to:

* integrate directly with AWS services

without manually managing IPs.

---

# AWS Alias Flow

```text id="v6m4w8"
Route 53 Alias
↓
ALB DNS Name
↓
Dynamic Infrastructure
```

---

# Benefits of Alias Records

| Benefit                 | Explanation                    |
| ----------------------- | ------------------------------ |
| Native AWS Integration  | Direct resource routing        |
| No Manual IP Management | Dynamic infrastructure support |
| Root Domain Support     | Apex domain routing            |
| Improved Performance    | No additional DNS lookup       |

---

# Alias Records in This Project

The project used:

* Route 53 Alias records
* Public ALB integration
* root domain routing

---

# 3. ALB DNS Integration

---

# Why ALB Integration Matters

ALBs:

* do not have fixed IP addresses

They use:

* AWS-managed DNS names

---

# ALB DNS Flow

```text id="q4m9x1"
b4n3xus.in
↓
Route 53 Alias
↓
Public ALB
↓
Web Tier
```

---

# Practical Implementation in This Project

Configured:

* Route 53 Public Hosted Zone
* Alias record
* Public ALB mapping

---

# Subdomain Experiments

The project also explored:

* subdomain creation
* CNAME routing
* host-based routing integration

---

# 4. Best Practices

---

# DNS Best Practices

| Best Practice                | Reason                     |
| ---------------------------- | -------------------------- |
| Use Alias for AWS Resources  | Better integration         |
| Use CNAME for Subdomains     | Flexible routing           |
| Avoid Hardcoding IPs         | Dynamic infrastructure     |
| Use Low TTL During Migration | Faster propagation         |
| Use Hosted Zones Properly    | Centralized DNS management |

---

# Enterprise DNS Best Practices

Enterprise systems commonly:

* separate environments
* use scalable DNS routing
* integrate DNS with Load Balancers
* implement failover-ready DNS architecture

---

# Best Practice Architecture

```text id="p8m3w6"
Route 53
↓
Alias Record
↓
ALB
↓
Scalable Infrastructure
```

---

# DNS Concepts Implemented in This Project

| Concept              | Implementation       |
| -------------------- | -------------------- |
| Public Hosted Zone   | b4n3xus.in           |
| Alias Record         | ALB integration      |
| CNAME                | Subdomain routing    |
| DNS Propagation      | Route testing        |
| Host-Based Routing   | Subdomain forwarding |
| Route 53 Integration | AWS-native DNS       |

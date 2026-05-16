# Volume 2 — AWS Networking, Security & IAM
## Chapter 1 — Amazon VPC

Amazon VPC (Virtual Private Cloud) is one of the most important AWS services because it forms the networking foundation of cloud infrastructure.

Almost every AWS architecture depends on VPC concepts such as:

IP addressing
subnetting
routing
internet access
private networking
security isolation

1. What is a VPC
Definition

Amazon VPC (Virtual Private Cloud) is a logically isolated virtual network inside AWS where cloud resources are deployed.

A VPC allows organizations to:

control networking
isolate infrastructure
configure routing
define IP ranges
manage internet access
secure workloads
Simple Explanation

A VPC is similar to creating a private data center inside AWS.

Inside the VPC, organizations can create:

subnets
servers
route tables
gateways
security configurations

while maintaining isolation from other AWS customers.

Real-World Analogy

Imagine an apartment complex.

AWS is the entire city.

Your VPC is:

your private apartment building

Inside the building, you decide:

room layout
security
access control
internal organization

Similarly, a VPC gives customers full control over their cloud network.

VPC Architecture Overview
AWS Cloud
↓
VPC
├── Public Subnets
├── Private Subnets
├── Route Tables
├── Internet Gateway
├── NAT Gateway
├── EC2 Instances
└── Security Layers
Core Components of a VPC
Component	Purpose
CIDR Block	Defines IP range
Subnets	Divide network logically
Route Tables	Control traffic routing
Internet Gateway	Internet connectivity
NAT Gateway	Secure outbound internet
Security Groups	Instance-level firewall
NACLs	Subnet-level security
Why VPC is Important

Without VPC:

workloads would not be isolated
traffic control would be limited
enterprise networking would be impossible
security segmentation would be weak

VPC enables:

private networking
traffic isolation
enterprise architecture
secure cloud deployments
VPC in This Project

This project used a custom VPC architecture to implement:

public subnets
private subnets
database isolation
NAT Gateway
Bastion Host
Multi-AZ deployment
layered security
High-Level Project VPC Flow
Internet
↓
Internet Gateway
↓
Public Subnets
↓
Web Tier
↓
Private App Subnets
↓
Database Subnets
2. Why VPC is Required
Problem Without VPC

If all cloud resources existed in a shared public network:

security risks increase
traffic isolation becomes difficult
internal communication becomes exposed
enterprise segmentation becomes impossible
VPC Solves These Problems

VPC provides:

network isolation
secure communication
traffic control
subnet segmentation
customizable routing
enterprise-grade networking
Enterprise Benefits of VPC
Benefit	Explanation
Isolation	Separate workloads securely
Security	Control inbound/outbound traffic
Scalability	Support large architectures
Flexibility	Custom network design
Availability	Multi-AZ deployments
Hybrid Connectivity	Connect on-premise infrastructure
Real-World Enterprise Example

A banking application may separate:

public web servers
backend services
databases

into different subnets for:

security
compliance
traffic isolation

This is achieved using VPC architecture.

Why a Custom VPC Was Used in This Project

AWS provides a default VPC automatically.

However, enterprise architectures rarely use default VPCs because they require:

custom subnet layouts
custom routing
private networking
controlled internet access
security segmentation

Therefore, a custom VPC was created.

Practical Implementation in This Project

The project implemented:

Feature	Purpose
Custom CIDR	Scalable IP planning
Public Subnets	Internet-facing services
Private App Subnets	Backend isolation
Private DB Subnets	Database security
NAT Gateway	Secure outbound access
Bastion Host	Controlled SSH access
3. VPC CIDR Planning
What is CIDR Planning

CIDR planning defines how IP ranges are allocated inside a VPC.

Example:

10.0.0.0/16

CIDR planning is extremely important because poor planning can:

limit scalability
create IP conflicts
complicate subnet expansion
break enterprise networking
CIDR Used in This Project

The VPC used:

10.0.0.0/16
Why /16 Was Chosen

A /16 CIDR provides:

65,536 IP addresses
large expansion capability
support for multiple subnet tiers
future scalability
CIDR Breakdown
CIDR	Number of IPs
/16	65,536
/24	256
/32	1
Enterprise CIDR Planning Principles

Good CIDR planning should support:

future growth
subnet expansion
multiple environments
multi-tier design
disaster recovery
Example Enterprise Layout
10.0.0.0/16
│
├── Public Subnets
├── App Subnets
├── Database Subnets
├── Management Subnets
└── Future Expansion
Poor CIDR Planning Problems

Improper CIDR design can cause:

subnet overlap
routing conflicts
difficult migrations
limited scalability
Subnet Allocation in This Project
Subnet	CIDR
Public-Subnet-1	10.0.1.0/24
Public-Subnet-2	10.0.2.0/24
Private-Subnet-1	10.0.3.0/24
Private-Subnet-2	10.0.4.0/24
DB-Subnet-1	10.0.5.0/24
DB-Subnet-2	10.0.6.0/24
Why Multiple Subnets Were Used

Multiple subnets improve:

availability
security
traffic isolation
fault tolerance

Each layer was separated logically.

4. Enterprise VPC Design
What is Enterprise VPC Design

Enterprise VPC design refers to building scalable, secure, and highly available network architectures.

Core Enterprise Design Principles

The architecture implemented several enterprise networking principles:

Principle	Purpose
Multi-AZ Deployment	High Availability
Public/Private Separation	Security
Layered Architecture	Traffic isolation
NAT-Based Internet Access	Private subnet protection
Bastion-Based Access	Controlled administration
Segmented Routing	Secure traffic flow
Multi-Tier Network Architecture

The architecture used a 3-tier model:

Public Layer
↓
Application Layer
↓
Database Layer
Public Layer

Contains:

Public ALB
Bastion Host
Internet-facing resources

Connected to:

Internet Gateway
Application Layer

Contains:

backend application servers
internal services

Protected using:

private subnets
internal ALB
Security Groups
Database Layer

Contains:

MySQL database EC2

Fully isolated from:

public internet access
Multi-AZ Design

Resources were distributed across:

us-east-1a
us-east-1b

to improve:

availability
redundancy
fault tolerance
Enterprise Networking Flow
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
Database Tier
Security Segmentation

Traffic was controlled using:

Security Groups
private subnets
route tables
internal ALB routing

This reduced unnecessary exposure.

Benefits of Enterprise VPC Design
Benefit	Explanation
High Availability	Multi-AZ deployment
Scalability	Easy subnet expansion
Security	Isolated workloads
Fault Isolation	Failure containment
Traffic Management	Controlled routing
5. Custom VPC Implementation
Why Custom VPC Was Implemented

A custom VPC was created to support:

enterprise architecture
subnet segmentation
custom routing
private networking
secure communication
VPC Configuration Used
Configuration	Value
Region	us-east-1
VPC CIDR	10.0.0.0/16
Availability Zones	us-east-1a, us-east-1b
Public Subnets	2
Private App Subnets	2
Private DB Subnets	2
VPC Architecture Implemented
VPC: 10.0.0.0/16
│
├── Public Subnet 1 (AZ-1)
├── Public Subnet 2 (AZ-2)
│
├── Private App Subnet 1
├── Private App Subnet 2
│
├── DB Subnet 1
└── DB Subnet 2
Internet Connectivity Design
Internet Gateway

Used for:

inbound internet access
public subnet communication

Attached to:

Public Route Table
NAT Gateway

Used for:

outbound internet access from private subnets

without exposing private instances publicly.

Bastion Host

The Bastion Host was placed in:

public subnet

Used for:

controlled SSH access
secure administration
Route Table Design
Route Table	Purpose
Public RT	Internet routing
Private RT	NAT Gateway routing
DB RT	Isolated database routing
High Availability Considerations

The VPC architecture was designed for:

Multi-AZ deployment
scalable infrastructure
Auto Scaling integration
load balancing support
Security Considerations

The design implemented:

subnet isolation
SG chaining
private networking
least privilege communication
Real-World Importance of VPC Design

Poor VPC architecture can lead to:

security vulnerabilities
scaling limitations
routing complexity
operational issues

Well-designed VPCs improve:

maintainability
scalability
security
reliability

## Chapter 2 — Subnet Architecture

Subnet architecture is one of the most important parts of AWS networking and enterprise cloud infrastructure design.

Subnets determine:

how resources are organized
how traffic flows
which resources are publicly accessible
which resources remain private
how security boundaries are enforced

A properly designed subnet architecture improves:

security
scalability
fault isolation
availability
traffic management

1. What is a Subnet
Definition

A subnet is a smaller logical network created inside a VPC.

Subnets divide a VPC into multiple isolated network sections.

Real-World Analogy

Imagine a large office building.

The building represents:

VPC

Different floors inside the building represent:

Subnets

Each floor can serve a different purpose:

reception
engineering
management
secure storage

Similarly, AWS subnets separate workloads logically.

Why Subnets Are Important

Subnets help:

organize infrastructure
isolate workloads
improve security
manage routing
separate public and private resources
High-Level Subnet Architecture
VPC
│
├── Public Subnets
├── Private Application Subnets
└── Private Database Subnets
Subnet Characteristics
Feature	Description
Exists Inside VPC	Subnets belong to a VPC
Uses CIDR Range	Each subnet has its own IP range
AZ-Specific	A subnet belongs to one Availability Zone
Route Table Association	Controls traffic flow
Subnets in This Project

The architecture implemented:

Subnet Type	Purpose
Public Subnets	Internet-facing resources
Private App Subnets	Backend application servers
Database Subnets	Database isolation
2. Public Subnets
What is a Public Subnet

A Public Subnet is a subnet that has a route to the Internet Gateway (IGW).

Resources inside public subnets can:

access the internet
receive inbound internet traffic
Public Subnet Flow
Internet
↓
Internet Gateway
↓
Public Route Table
↓
Public Subnet
Why Public Subnets Are Required

Some resources must be accessible from the internet.

Examples:

Load Balancers
Bastion Hosts
Web servers
Public APIs
Resources Placed in Public Subnets in This Project
Resource	Purpose
Public ALB	Internet-facing traffic distribution
Bastion Host	Secure SSH administration
Web Tier	Frontend communication
Public Subnet CIDRs Used
Subnet	CIDR	AZ
Public-Subnet-1	10.0.1.0/24	us-east-1a
Public-Subnet-2	10.0.2.0/24	us-east-1b
Public Route Table Example
0.0.0.0/0 → Internet Gateway

This means:

internet traffic is routed through the IGW.
Enterprise Considerations for Public Subnets

Public subnets should contain only resources requiring internet exposure.

Sensitive resources should NEVER be directly exposed publicly.

Common Beginner Mistake

IMPORTANT:
Beginners often place databases inside public subnets.

This creates major security risks.

Databases should remain private unless absolutely necessary.

3. Private Subnets
What is a Private Subnet

A Private Subnet does NOT have direct internet access through an Internet Gateway.

Resources inside private subnets:

cannot receive direct internet traffic
remain isolated from public access
Why Private Subnets Are Important

Private subnets improve:

security
workload isolation
internal communication protection

Most enterprise backend systems operate inside private subnets.

Private Subnet Architecture Flow
Private EC2
↓
Private Route Table
↓
NAT Gateway
↓
Internet Gateway
↓
Internet
Key Characteristic

Private instances:

can access the internet outbound using NAT
cannot be accessed directly from the internet
Resources Placed in Private App Subnets
Resource	Purpose
Backend Application Servers	Internal business logic
APIs	Internal communication
Internal Services	Secure backend workloads
Private App Subnets Used in This Project
Subnet	CIDR	AZ
Private-Subnet-1	10.0.3.0/24	us-east-1a
Private-Subnet-2	10.0.4.0/24	us-east-1b
Why Backend Servers Were Kept Private

The application tier handled:

API processing
backend logic
database communication

These services should not be publicly exposed.

Instead:

traffic passed through Internal ALB
SG chaining controlled communication
Enterprise Security Benefits

Private subnets reduce:

attack surface
unauthorized access
direct exposure

This is a standard enterprise security practice.

NAT Gateway Usage

Private instances still required internet access for:

package installation
updates
dependency downloads

Therefore:

NAT Gateway was implemented.
Practical NAT Flow in This Project
Private App Server
↓
NAT Gateway
↓
Internet

without exposing the app server publicly.

4. Database Subnets
What is a Database Subnet

Database subnets are isolated private subnets dedicated to database workloads.

These subnets provide:

additional security
workload isolation
controlled access
Why Database Isolation Is Important

Databases contain:

application data
credentials
sensitive information

Direct public access creates severe security risks.

Database Architecture Flow
Application Tier
↓
Database Security Group
↓
Database Subnet
↓
MySQL EC2
Database Subnets Used in This Project
Subnet	CIDR	AZ
DB-Subnet-1	10.0.5.0/24	us-east-1a
DB-Subnet-2	10.0.6.0/24	us-east-1b
Database Design Used

The project used:

MySQL hosted on EC2

instead of:

Amazon RDS

This helped provide deeper understanding of:

database installation
Linux administration
MySQL networking
DB security configuration
Why Only Private Access Was Allowed

Database access was restricted to:

application tier
Bastion Host (administrative access)

using:

Security Groups
private routing
Enterprise Database Security Principles

Databases should:

remain private
avoid direct internet exposure
allow restricted access only
use layered security
Common Beginner Mistakes
Mistake	Risk
Public DB exposure	Security breach
Wide-open SG rules	Unauthorized access
Shared subnet usage	Poor isolation
5. Multi-Tier Subnet Segmentation
What is Multi-Tier Segmentation

Multi-tier segmentation separates infrastructure into logical layers.

This architecture used:

Presentation Layer
↓
Application Layer
↓
Database Layer

Each layer used separate subnets.

Why Multi-Tier Architecture Is Important

Benefits include:

improved security
traffic isolation
scalability
easier troubleshooting
better workload management
Multi-Tier Architecture in This Project
Tier	Subnet Type
Web Tier	Public Subnets
App Tier	Private App Subnets
Database Tier	DB Subnets
Request Flow Example
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
Database Tier
Security Segmentation

Communication between layers was controlled using:

Security Groups
Route Tables
Internal ALB
Security Group Chaining
ALB SG
↓
Web SG
↓
Internal ALB SG
↓
App SG
↓
DB SG

This is a strong enterprise security model.

Enterprise Advantages of Multi-Tier Segmentation
Benefit	Explanation
Security	Reduced exposure
Isolation	Separate workloads
Scalability	Independent scaling
Fault Isolation	Failure containment
Traffic Control	Controlled communication
6. Multi-AZ Subnet Design
What is Multi-AZ Design

Multi-AZ architecture distributes infrastructure across multiple Availability Zones.

This improves:

availability
redundancy
fault tolerance
Why Multi-AZ Is Important

If one AZ fails:

resources in another AZ continue operating

This minimizes downtime.

AZs Used in This Project
us-east-1a
us-east-1b
Multi-AZ Subnet Layout
AZ-1
├── Public Subnet 1
├── Private App Subnet 1
└── DB Subnet 1

AZ-2
├── Public Subnet 2
├── Private App Subnet 2
└── DB Subnet 2
High Availability Strategy

The architecture implemented:

redundant web servers
redundant app servers
ALB traffic distribution
Multi-AZ deployment
Multi-AZ Traffic Flow
User
↓
ALB
↓
AZ-1 Instance
AZ-2 Instance

ALB distributes traffic across healthy targets.

Enterprise Benefits of Multi-AZ Design
Benefit	Explanation
High Availability	Reduced downtime
Redundancy	Backup infrastructure
Fault Tolerance	AZ failure survivability
Scalability	Distributed workloads
Practical Multi-AZ Design in This Project

The project implemented:

public subnets across 2 AZs
private subnets across 2 AZs
redundant web tier
redundant application tier

This supported:

HA architecture
future Auto Scaling
load-balanced traffic distribution

# Chapter 3 — Route Tables & Routing

Routing is one of the most important concepts in cloud networking and AWS infrastructure design.

Routing determines:

where network traffic should go
how systems communicate
which resources can access the internet
how private communication works
how traffic isolation is enforced

In AWS, routing is primarily controlled using:

Route Tables
Internet Gateway
NAT Gateway
local VPC routing

1. What is Routing
Definition

Routing is the process of directing network traffic from one destination to another.

Routing determines:

where packets should travel
which gateway should handle traffic
how networks communicate
Real-World Analogy

Routing is similar to road navigation.

Example:

Home Address
↓
Road Network
↓
Destination

In networking:

Source Server
↓
Route Table
↓
Gateway
↓
Destination
Why Routing Is Important

Without routing:

systems cannot communicate
internet access fails
subnet communication breaks
enterprise networking becomes impossible

Routing enables:

internet connectivity
private communication
traffic segmentation
secure infrastructure design
Routing in This Project

The project implemented:

public routing
private routing
NAT-based outbound routing
database isolation routing
segmented traffic flow
High-Level Routing Flow
Internet
↓
Internet Gateway
↓
Public Route Table
↓
Public Subnets
↓
Private Route Table
↓
Private Subnets
2. Route Tables
What is a Route Table

A Route Table is a collection of routing rules that determines where network traffic should be directed.

Every subnet in AWS is associated with a Route Table.

Simple Explanation

A Route Table acts like:

a traffic control map

It tells AWS:

where packets should go
which gateway to use
how traffic should leave the subnet
Route Table Components
Component	Purpose
Destination	Target network
Target	Gateway or route destination
Example Route Table Entry
Destination: 0.0.0.0/0
Target: Internet Gateway

Meaning:

all internet traffic goes through IGW
Local Route

Every VPC automatically includes a local route.

Example:

10.0.0.0/16 → local

This allows:

internal VPC communication
Route Tables Used in This Project
Route Table	Purpose
Public Route Table	Internet access
Private Route Table	NAT routing
DB Route Table	Database isolation
Route Table Architecture
Route Tables
│
├── Public RT
├── Private RT
└── DB RT
Why Multiple Route Tables Were Used

Separate route tables improve:

security
traffic isolation
subnet segmentation
enterprise traffic management
3. Static Routing
What is Static Routing

Static routing means manually defining traffic routes.

AWS Route Tables primarily use static routing.

Example
0.0.0.0/0 → NAT Gateway

This route is manually configured.

Advantages of Static Routing
Advantage	Explanation
Predictable	Fixed traffic behavior
Simple	Easy to configure
Controlled	Explicit traffic flow
Secure	Better traffic isolation
Static Routing in This Project

The project manually configured:

internet routes
NAT routes
subnet associations
isolated DB routing
Enterprise Use of Static Routing

Static routing is commonly used in:

VPC architectures
segmented cloud networks
secure enterprise environments

because:

traffic paths remain predictable
4. Default Routes
What is a Default Route

A default route handles traffic when no more specific route exists.

In AWS:

0.0.0.0/0

represents:

all IPv4 internet traffic
Example
0.0.0.0/0 → Internet Gateway

Meaning:

all unknown traffic goes to the internet
Why Default Routes Are Important

Without default routes:

internet communication fails
outbound traffic cannot leave subnets
Default Route in Public Route Table
0.0.0.0/0 → IGW

Used for:

public internet access
Default Route in Private Route Table
0.0.0.0/0 → NAT Gateway

Used for:

secure outbound internet access
Difference Between Public and Private Default Routing
Route	Purpose
IGW Route	Direct internet access
NAT Route	Outbound-only internet access
5. Internet Routing
What is Internet Routing

Internet routing enables AWS resources to communicate with the public internet.

This requires:

Internet Gateway
public IP addresses
proper Route Table configuration
Internet Routing Flow
Internet
↓
Internet Gateway
↓
Public Route Table
↓
Public Subnet
↓
Public EC2 / ALB
Internet Gateway (IGW)

An Internet Gateway is attached to the VPC to enable internet communication.

Why IGW Is Required

Without IGW:

public resources cannot access the internet
inbound internet traffic cannot reach AWS resources
Public Resources in This Project
Resource	Reason
Public ALB	Internet-facing traffic
Bastion Host	SSH access
Web Tier	Frontend communication
Public Route Table in This Project
Destination: 0.0.0.0/0
Target: Internet Gateway

Associated with:

Public-Subnet-1
Public-Subnet-2
Public Routing Diagram
Internet
↓
IGW
↓
Public RT
↓
Public Subnet
↓
ALB / Bastion
Common Beginner Mistake

IMPORTANT:
Adding an Internet Gateway alone does NOT make a subnet public.

The subnet also requires:

public route table association
default route to IGW
public IP assignment
6. Private Routing
What is Private Routing

Private routing allows internal communication while preventing direct public internet exposure.

Private subnets:

do not route directly to IGW

Instead:

outbound traffic goes through NAT Gateway
Why Private Routing Is Important

Private routing protects:

backend servers
databases
internal APIs

from direct internet access.

Private Routing Flow
Private EC2
↓
Private RT
↓
NAT Gateway
↓
Internet Gateway
↓
Internet
Why NAT Gateway Was Used

Private servers required outbound internet access for:

package installation
updates
dependency downloads

However:

they should remain private

NAT Gateway solved this problem.

Private Route Table in This Project
Destination: 0.0.0.0/0
Target: NAT Gateway

Associated with:

Private-Subnet-1
Private-Subnet-2
Private Routing Benefits
Benefit	Explanation
Security	No direct internet exposure
Controlled Access	Outbound-only internet access
Isolation	Backend protection
Enterprise Compliance	Secure infrastructure design
Internal Traffic Flow

The application architecture used:

Internal ALB
private subnet routing
SG-controlled communication
Internal Request Flow
Web Tier
↓
Internal ALB
↓
Private App Tier

This improved:

security
backend isolation
controlled communication
7. Database Routing Isolation
Why Database Isolation Is Important

Databases contain:

sensitive data
credentials
business information

Therefore:

databases should remain isolated
Database Routing Design

Database subnets:

had isolated route tables
avoided direct internet routing
DB Routing Flow
Application Tier
↓
DB Security Group
↓
DB Route Table
↓
Database Subnet
Database Route Table

The DB Route Table included:

local VPC communication only

This prevented:

direct internet communication
Why DB Isolation Matters

Benefits:

stronger security
reduced attack surface
controlled access
enterprise-grade protection
Database Communication in This Project

Only:

App Tier
Bastion Host

could communicate with the database.

Access was controlled using:

Security Groups
private routing
subnet isolation
Enterprise Database Best Practices

Databases should:

remain private
avoid public IPs
use SG-based restrictions
allow minimal access only
Common Beginner Mistakes
Mistake	Risk
Public database access	Security breach
Shared route tables	Poor isolation
Wide-open SG rules	Unauthorized access
Routing Architecture in This Project
Public Routing
0.0.0.0/0 → IGW

Used for:

Public ALB
Bastion Host
Web Tier
Private Routing
0.0.0.0/0 → NAT Gateway

Used for:

App Tier
Database Routing
10.0.0.0/16 → local

Used for:

isolated DB communication
Complete Routing Architecture
Internet
↓
Internet Gateway
↓
Public Route Table
↓
Public Subnets
↓
Internal Communication
↓
Private Route Table
↓
Private App Subnets
↓
DB Route Table
↓
Database Subnets

## Chapter 4 — Internet Gateway & NAT Gateway

Internet connectivity is one of the most important aspects of AWS networking architecture.

Some AWS resources require:

public internet access
inbound internet communication
outbound internet communication

At the same time, enterprise architectures must also ensure:

backend isolation
secure private networking
controlled internet exposure

AWS provides:

Internet Gateway (IGW)
NAT Gateway

to manage secure internet communication.

Why Internet Connectivity Matters

Modern cloud infrastructure requires internet communication for:

web hosting
software updates
package downloads
API communication
public applications

However, not all resources should be directly exposed publicly.

Enterprise architectures therefore separate:

public internet access
private outbound access

using:

Internet Gateway
NAT Gateway
High-Level Internet Architecture
Internet
↓
Internet Gateway
↓
Public Subnets
↓
NAT Gateway
↓
Private Subnets
1. Internet Gateway (IGW)
What is an Internet Gateway

An Internet Gateway (IGW) is a VPC component that allows communication between:

AWS resources
the public internet

It enables:

inbound internet traffic
outbound internet traffic
Simple Explanation

An Internet Gateway acts as:

the main entry and exit point between AWS infrastructure and the internet.
Real-World Analogy

Imagine a secured office building.

The Internet Gateway acts as:

the main gate connecting the building to the outside world.

Without the gate:

people cannot enter or leave.

Similarly:

AWS resources cannot communicate with the internet without IGW.
Internet Gateway Architecture
Internet
↓
Internet Gateway
↓
Public Route Table
↓
Public Subnet
Key Functions of Internet Gateway
Function	Purpose
Internet Access	Enables public communication
Inbound Traffic	Allows users to access resources
Outbound Traffic	Allows AWS resources to access internet
Route Target	Used in Route Tables
Important Requirement for Internet Access

To make a subnet public, the following are required:

Requirement	Purpose
Internet Gateway	Internet connectivity
Public Route	Route to IGW
Public IP	Internet-reachable address

All three are necessary.

Internet Gateway in This Project

The architecture attached:

one Internet Gateway

to:

Production-VPC

Used for:

public ALB communication
Bastion Host access
frontend internet traffic
Public Internet Connectivity
What is Public Internet Connectivity

Public internet connectivity allows resources to:

receive internet requests
communicate publicly
host web applications
Public Connectivity Flow
User
↓
Internet
↓
Internet Gateway
↓
Public Subnet
↓
Public Resource
Public Resources in This Project
Resource	Reason
Public ALB	Internet-facing traffic
Bastion Host	Administrative SSH access
Web Tier	Frontend traffic handling
Public ALB Architecture
User
↓
Internet
↓
Public ALB
↓
Web Tier

The ALB received:

HTTP traffic
internet requests

and distributed traffic to backend targets.

Public Route Table Configuration

The Public Route Table contained:

Destination: 0.0.0.0/0
Target: Internet Gateway

Meaning:

all internet traffic routes through IGW.
Public Subnet Design

The following subnets were public:

Subnet	CIDR
Public-Subnet-1	10.0.1.0/24
Public-Subnet-2	10.0.2.0/24

These subnets hosted:

ALB
Bastion Host
Web Tier
Common Beginner Mistake

IMPORTANT:
Creating an Internet Gateway alone does NOT automatically provide internet access.

The subnet must also:

use a Route Table with IGW route
have public IP assignment enabled
Security Considerations for Public Resources

Public resources should:

expose only required ports
use Security Groups
avoid unnecessary public access
Example Security Group Rules
Port	Purpose
80	HTTP
443	HTTPS
22	SSH (restricted)
2. NAT Gateway
What is a NAT Gateway

A NAT Gateway allows private subnet resources to access the internet securely without becoming publicly accessible.

Why NAT Gateway Is Required

Private instances often need internet access for:

package installation
software updates
dependency downloads
external API communication

However:

these instances should remain private

NAT Gateway solves this problem.

NAT Gateway Architecture
Private EC2
↓
Private Route Table
↓
NAT Gateway
↓
Internet Gateway
↓
Internet
Key Characteristic of NAT Gateway

NAT Gateway allows:

outbound internet communication

but blocks:

inbound internet initiation

This protects private infrastructure.

Simple Real-World Analogy

Imagine employees inside a secure office.

Employees can:

go outside when needed

But outsiders:

cannot directly enter internal secure areas.

NAT works similarly.

NAT Gateway Placement

A NAT Gateway must be placed in:

a public subnet

because it requires:

internet connectivity through IGW.
NAT Gateway Components
Component	Purpose
Elastic IP	Public internet communication
Public Subnet	Internet reachability
Route Table Association	Traffic routing
NAT Gateway in This Project

The architecture used:

NAT Gateway for private app subnets

This allowed:

secure outbound internet access
package installation
software updates

without exposing app servers publicly.

Practical NAT Usage in This Project

Private app servers used NAT for:

Node.js dependency installation
system updates
backend package downloads
Private Outbound Internet Access
What is Private Outbound Access

Private outbound internet access means:

private instances can access the internet
internet cannot directly initiate communication back
Private Routing Flow
Private App Server
↓
NAT Gateway
↓
Internet
Why This Is Important

This architecture provides:

internet functionality
backend isolation
reduced attack surface
Private Resources in This Project
Resource	Access Type
App Tier	Private
Database Tier	Private
Internal APIs	Private
NAT Route Table Configuration

The Private Route Table included:

Destination: 0.0.0.0/0
Target: NAT Gateway

Associated with:

Private App Subnets
Difference Between IGW and NAT Gateway
Feature	Internet Gateway	NAT Gateway
Public Access	Yes	No
Inbound Internet Traffic	Allowed	Blocked
Outbound Internet Traffic	Allowed	Allowed
Used In	Public Subnets	Private Subnets
Enterprise Security Importance

Using NAT Gateways:

protects backend systems
prevents direct exposure
supports secure internet access

This is a standard enterprise architecture pattern.

Common Beginner Mistakes
Mistake	Problem
Placing NAT in private subnet	NAT becomes unreachable
Missing NAT route	No internet access
Public backend servers	Increased attack surface
3. Secure Internet Communication for Private Instances
Why Private Instances Need Internet Access

Private servers still require internet access for:

updates
patches
dependency installation
external API calls
Why They Should Remain Private

Backend systems often contain:

business logic
internal APIs
sensitive communication
database access

Direct internet exposure increases risk.

Enterprise Security Model

Enterprise architectures commonly use:

Public Layer
↓
Private Layer
↓
Database Layer

Only the public layer is internet-facing.

Secure Communication Architecture in This Project
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

This architecture:

protected backend services
isolated database communication
reduced public exposure
Bastion Host and Private Access

Administrative SSH access to private instances was performed using:

Bastion Host

This avoided:

exposing private servers publicly
Bastion Access Flow
Administrator
↓
Bastion Host
↓
Private EC2
Security Benefits of This Architecture
Security Feature	Benefit
NAT Gateway	Secure outbound internet
Private Subnets	Backend isolation
Bastion Host	Controlled SSH access
Internal ALB	Internal traffic protection
SG Chaining	Layered security
Internet Connectivity Architecture in This Project
Public Internet Flow
Internet
↓
IGW
↓
Public ALB
↓
Web Tier
Private Internet Flow
Private App Server
↓
NAT Gateway
↓
IGW
↓
Internet
Database Isolation Flow
App Tier
↓
DB Security Group
↓
Database Tier

No direct internet communication existed.

## Chapter 5 — Security Groups

Security is one of the most critical aspects of cloud infrastructure design.

In AWS, Security Groups (SGs) act as virtual firewalls that control traffic flowing to and from resources.

Security Groups are fundamental for:

securing EC2 instances
controlling communication
isolating workloads
implementing least privilege access
building enterprise-grade architectures

1. What is a Security Group
Definition

A Security Group (SG) is a virtual firewall attached to AWS resources that controls:

inbound traffic
outbound traffic

Security Groups are commonly attached to:

EC2 instances
Load Balancers
databases
ENIs (Elastic Network Interfaces)
Simple Explanation

Security Groups determine:

who can communicate with a resource
which ports are accessible
what type of traffic is allowed
Real-World Analogy

Imagine a secured office building.

The Security Group acts like:

a security guard at the entrance

The guard checks:

who can enter
which rooms can be accessed
what communication is permitted

Similarly:

SGs control network communication.
Security Group Architecture
Internet
↓
Security Group
↓
EC2 Instance
Why Security Groups Are Important

Without Security Groups:

resources become exposed
unauthorized communication becomes possible
enterprise isolation breaks down

Security Groups provide:

traffic filtering
workload isolation
controlled communication
security segmentation
Security Groups in This Project

The project implemented:

multiple SG layers
SG chaining
controlled east-west communication
least privilege traffic flow
High-Level SG Flow
Public ALB SG
↓
Web Tier SG
↓
Internal ALB SG
↓
App Tier SG
↓
Database SG
2. Stateful Firewall Concepts
What is a Stateful Firewall

A stateful firewall remembers active connections.

This means:

return traffic is automatically allowed

if the initial request was permitted.

Example

Suppose:

inbound HTTP traffic on port 80 is allowed

When the server responds:

outbound response traffic is automatically allowed

even without explicit outbound rules.

Stateful Communication Flow
Client Request
↓
Security Group
↓
Server Response Automatically Allowed
Why Stateful Firewalls Are Important

Stateful firewalls simplify:

traffic management
return communication
enterprise firewall configuration
Security Groups Are Stateful

AWS Security Groups are:

stateful firewalls

This is one of their most important characteristics.

Difference Between Stateful and Stateless
Feature	Stateful	Stateless
Tracks Connections	Yes	No
Automatic Return Traffic	Yes	No
Simpler Configuration	Yes	No
Example	Security Groups	NACLs
Example in This Project

When:

ALB forwarded requests to Web Tier

the return traffic was automatically allowed because:

Security Groups are stateful.
3. Inbound and Outbound Rules
Inbound Rules

Inbound rules control:

incoming traffic

to a resource.

Example
Port 80 → Allow HTTP traffic

This allows:

users to access web servers.
Outbound Rules

Outbound rules control:

outgoing traffic

from a resource.

Example
Allow traffic to Database Port 3306

This allows:

application servers to communicate with databases.
Security Group Rule Components
Component	Purpose
Protocol	TCP/UDP
Port	Service port
Source/Destination	Traffic origin
Allow Rule	Permitted communication
Common Ports Used in This Project
Port	Purpose
22	SSH
80	HTTP
4000	Backend API
3306	MySQL
Example Security Group Rules
Web Tier SG
Type	Port	Source
HTTP	80	Public ALB SG
SSH	22	Bastion SG
App Tier SG
Type	Port	Source
API	4000	Internal ALB SG
Database SG
Type	Port	Source
MySQL	3306	App Tier SG
Why Restrictive Rules Matter

Restrictive SG rules reduce:

attack surface
unauthorized communication
accidental exposure

This follows:

least privilege security principles
Common Beginner Mistake

IMPORTANT:
Beginners often allow:

0.0.0.0/0

for all ports.

This creates major security risks.

Only required ports should be exposed.

4. SG-to-SG Communication
What is SG-to-SG Communication

Security Groups can reference other Security Groups instead of using IP addresses.

This allows:

secure service-to-service communication
dynamic infrastructure communication
scalable security design
Example

Instead of:

Allow:
10.0.3.10

AWS allows:

Allow:
App-Tier-SG

This is more scalable.

Why SG-to-SG Communication Is Powerful

Benefits:

dynamic scaling support
easier infrastructure management
automatic instance handling
enterprise flexibility
Example Architecture
Web SG
↓
App SG
↓
DB SG

Each layer trusts only specific SGs.

SG Communication in This Project
Public ALB SG

Allowed:

HTTP traffic from internet

Forwarded traffic to:

Web Tier SG
Web Tier SG

Allowed:

traffic only from ALB SG

Forwarded traffic to:

Internal ALB SG
App Tier SG

Allowed:

backend API traffic only from Internal ALB SG
Database SG

Allowed:

MySQL traffic only from App Tier SG
Enterprise Advantage of SG References

Using SG references instead of IPs:

simplifies scaling
supports Auto Scaling
avoids manual IP updates
5. Security Group Chaining
What is Security Group Chaining

Security Group chaining means:

layered SG communication between infrastructure tiers

Each tier communicates only with the next required tier.

Security Chain in This Project
Internet
↓
Public ALB SG
↓
Web Tier SG
↓
Internal ALB SG
↓
App Tier SG
↓
Database SG
Why SG Chaining Is Important

Benefits:

layered security
reduced exposure
controlled communication
enterprise-grade isolation
Example

The database:

trusted only App Tier SG

NOT:

internet traffic
public subnets
external systems

This significantly improved security.

Enterprise Security Principle

This architecture follows:

Zero Trust Networking

Meaning:

every communication must be explicitly allowed.
Benefits of SG Chaining
Benefit	Explanation
Layered Security	Multiple protection layers
Isolation	Controlled traffic flow
Reduced Attack Surface	Minimal exposure
Easier Troubleshooting	Clear communication paths
Common Beginner Mistakes
Mistake	Problem
Using 0.0.0.0/0 everywhere	Excessive exposure
Flat SG design	Poor isolation
Public DB access	Major security risk
6. Layered Security
What is Layered Security

Layered security means:

multiple security controls protect infrastructure

instead of relying on a single protection mechanism.

Enterprise Layered Security Model
Internet
↓
ALB SG
↓
Web SG
↓
Internal ALB SG
↓
App SG
↓
DB SG

Each layer adds protection.

Why Layered Security Is Important

If one layer fails:

other layers still protect infrastructure.
Layered Security Components in This Project
Layer	Protection
Public ALB	Internet filtering
Web Tier SG	Frontend protection
Internal ALB	Internal traffic control
App Tier SG	Backend isolation
DB SG	Database protection
Additional Security Layers Used

The project also used:

private subnets
NAT Gateway
Bastion Host
Route Table isolation
Defense in Depth

This layered model is called:

Defense in Depth

widely used in enterprise cybersecurity.

7. Enterprise Firewall Design
Enterprise Firewall Principles

Enterprise firewall architecture should:

minimize exposure
isolate workloads
allow only required communication
support scalability
follow least privilege
Firewall Design in This Project

The project implemented:

SG segmentation
SG chaining
subnet isolation
private networking
restricted DB access
Communication Model
Source	Destination	Allowed?
Internet	Public ALB	Yes
Internet	App Tier	No
Web Tier	App Tier	Yes
App Tier	Database	Yes
Internet	Database	No
Why This Design Is Strong

This architecture:

prevents direct backend exposure
protects databases
controls internal traffic
reduces attack surface
Real-World Enterprise Example

Banking applications commonly use:

multiple firewall layers
isolated backend systems
restricted database communication

similar to this architecture.

Security Architecture Used in This Project
Internet
↓
ALB
↓
Web Tier
↓
Internal ALB
↓
App Tier
↓
Database

Each communication step used:

Security Groups
controlled routing
subnet isolation


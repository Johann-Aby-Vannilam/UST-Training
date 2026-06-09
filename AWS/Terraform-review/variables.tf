variable "aws_region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability Zones for deployment."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the public subnets."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for the private subnets."
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "frontend_instance_type" {
  description = "EC2 instance type for the frontend EC2 instance."
  type        = string
  default     = "t3.small"
}

variable "backend_instance_type" {
  description = "EC2 instance type for the backend EC2 instance."
  type        = string
  default     = "t3.small"
}

variable "frontend_asg_min_size" {
  description = "Minimum number of frontend instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "frontend_asg_max_size" {
  description = "Maximum number of frontend instances in the Auto Scaling Group."
  type        = number
  default     = 2
}

variable "frontend_asg_desired_capacity" {
  description = "Desired number of frontend instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "backend_asg_min_size" {
  description = "Minimum number of backend instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "backend_asg_max_size" {
  description = "Maximum number of backend instances in the Auto Scaling Group."
  type        = number
  default     = 2
}

variable "backend_asg_desired_capacity" {
  description = "Desired number of backend instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "key_name" {
  description = "Optional EC2 key pair name for SSH access. Leave blank to skip."
  type        = string
  default     = ""
}

variable "db_name" {
  description = "Initial database name for RDS."
  type        = string
  default     = "fleetops"
}

variable "db_username" {
  description = "Master username for RDS."
  type        = string
  default     = "fleetops"
}

variable "db_password" {
  description = "Master password for RDS (sensitive). Set via CLI or TF vars file."
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance class."
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage (GB) for the RDS instance."
  type        = number
  default     = 20
}

variable "domain_name" {
  description = "Optional custom domain for the CloudFront distribution (e.g. example.com)."
  type        = string
  default     = ""
}

variable "hosted_zone_id" {
  description = "Route53 hosted zone ID for the domain (required for DNS validation and record creation)."
  type        = string
  default     = ""
}

variable "certificate_arn" {
  description = "Optional existing ACM certificate ARN (in us-east-1) to use for CloudFront/ALB. If empty, Terraform will request one when domain_name and hosted_zone_id are provided."
  type        = string
  default     = ""
}

variable "enable_waf" {
  description = "Enable AWS WAF for CloudFront (managed rule)."
  type        = bool
  default     = true
}

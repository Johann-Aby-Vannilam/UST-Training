provider "aws" {
  region = var.aws_region
}

# Provider alias for global services (ACM for CloudFront and WAF)
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

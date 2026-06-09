output "vpc_id" {
  description = "The VPC id."
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "The public subnet ids."
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "The private subnet ids."
  value       = aws_subnet.private[*].id
}

output "alb_dns_name" {
  description = "The public Application Load Balancer DNS name."
  value       = aws_lb.public.dns_name
}

output "cloudfront_domain_name" {
  description = "The CloudFront distribution domain name."
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "frontend_asg_name" {
  description = "The frontend Auto Scaling Group name."
  value       = aws_autoscaling_group.frontend.name
}

output "backend_asg_name" {
  description = "The backend Auto Scaling Group name."
  value       = aws_autoscaling_group.backend.name
}

output "rds_endpoint" {
  description = "RDS Postgres endpoint address."
  value       = aws_db_instance.postgres.address
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "fleetops-vpc"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "fleetops-igw"
  }
}

data "aws_ami" "ubuntu_backend" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
}

data "aws_ami" "ubuntu_frontend" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "fleetops-public-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  tags = {
    Name = "fleetops-private-subnet-${count.index + 1}"
  }
}

resource "aws_eip" "nat" {
  domain = "vpc"
  tags = {
    Name = "fleetops-nat-eip"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id
  tags = {
    Name = "fleetops-nat-gateway"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "fleetops-public-rt"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
  tags = {
    Name = "fleetops-private-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

data "aws_caller_identity" "current" {}

resource "aws_kms_key" "rds" {
  description             = "KMS key for encrypting FleetOps RDS data"
  deletion_window_in_days = 30

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Allow administration of the key",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
      },
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "Allow RDS use of the key",
      "Effect": "Allow",
      "Principal": {
        "Service": "rds.amazonaws.com"
      },
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
      ],
      "Resource": "*"
    }
  ]
}
POLICY
}

resource "aws_kms_alias" "rds" {
  name          = "alias/fleetops-rds"
  target_key_id = aws_kms_key.rds.key_id
}

resource "aws_iam_role" "ec2_ssm" {
  name               = "fleetops-ec2-ssm-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_policy_attachment" "ec2_ssm" {
  name       = "fleetops-ec2-ssm-attachment"
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  roles      = [aws_iam_role.ec2_ssm.name]
}

resource "aws_iam_instance_profile" "ec2_ssm" {
  name = "fleetops-ec2-ssm-profile"
  role = aws_iam_role.ec2_ssm.name
}

data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_security_group" "alb" {
  name        = "fleetops-alb-sg"
  description = "Allow HTTP/HTTPS to the ALB from the internet."
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "fleetops-alb-sg"
  }
}

resource "aws_security_group" "frontend" {
  name        = "fleetops-frontend-sg"
  description = "Allow frontend EC2 traffic from the ALB."
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow traffic from the ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "fleetops-frontend-sg"
  }
}

resource "aws_security_group" "backend" {
  name        = "fleetops-backend-sg"
  description = "Allow backend traffic from the internal ALB."
  vpc_id      = aws_vpc.main.id
  ingress {
    description     = "Allow API traffic from internal ALB on auth port 8081"
    from_port       = 8081
    to_port         = 8081
    protocol        = "tcp"
    security_groups = [aws_security_group.internal_alb.id]
  }
  ingress {
    description     = "Allow API traffic from internal ALB on vehicle port 8082"
    from_port       = 8082
    to_port         = 8082
    protocol        = "tcp"
    security_groups = [aws_security_group.internal_alb.id]
  }
  ingress {
    description     = "Allow API traffic from internal ALB on maintenance port 8083"
    from_port       = 8083
    to_port         = 8083
    protocol        = "tcp"
    security_groups = [aws_security_group.internal_alb.id]
  }
  ingress {
    description     = "Allow API traffic from internal ALB on request port 8084"
    from_port       = 8084
    to_port         = 8084
    protocol        = "tcp"
    security_groups = [aws_security_group.internal_alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "fleetops-backend-sg"
  }
}

resource "aws_security_group" "internal_alb" {
  name        = "fleetops-internal-alb-sg"
  description = "Security group for internal ALB allowing frontend to send traffic."
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow HTTP from frontend instances"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.frontend.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "fleetops-internal-alb-sg"
  }
}

resource "aws_lb" "public" {
  name               = "fleetops-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = false
  tags = {
    Name = "fleetops-alb"
  }
}

resource "aws_lb" "internal" {
  name               = "fleetops-internal-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.internal_alb.id]
  subnets            = aws_subnet.private[*].id

  enable_deletion_protection = false
  tags = {
    Name = "fleetops-internal-alb"
  }
}

resource "aws_lb_listener" "internal_http" {
  load_balancer_arn = aws_lb.internal.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_auth.arn
  }
}

resource "aws_lb_target_group" "frontend" {
  name        = "fleetops-frontend-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }
}

resource "aws_lb_target_group" "backend_auth" {
  name        = "fleetops-backend-auth-tg"
  port        = 8081
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/actuator/health"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }
}

resource "aws_lb_target_group" "backend_vehicle" {
  name        = "fleetops-backend-vehicle-tg"
  port        = 8082
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/actuator/health"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }
}

resource "aws_lb_target_group" "backend_maintenance" {
  name        = "fleetops-backend-maintenance-tg"
  port        = 8083
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/actuator/health"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }
}

resource "aws_lb_target_group" "backend_request" {
  name        = "fleetops-backend-request-tg"
  port        = 8084
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/actuator/health"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }
}


resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.public.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}

resource "aws_lb_listener_rule" "backend_auth" {
  listener_arn = aws_lb_listener.internal_http.arn
  priority     = 10

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_auth.arn
  }

  condition {
    path_pattern {
      values = ["/auth/*"]
    }
  }
}

resource "aws_lb_listener_rule" "backend_vehicle" {
  listener_arn = aws_lb_listener.internal_http.arn
  priority     = 20

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_vehicle.arn
  }

  condition {
    path_pattern {
      values = ["/api/vehicles*"]
    }
  }
}

resource "aws_lb_listener_rule" "backend_maintenance" {
  listener_arn = aws_lb_listener.internal_http.arn
  priority     = 30

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_maintenance.arn
  }

  condition {
    path_pattern {
      values = ["/api/tasks*"]
    }
  }
}

resource "aws_lb_listener_rule" "backend_request" {
  listener_arn = aws_lb_listener.internal_http.arn
  priority     = 40

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_request.arn
  }

  condition {
    path_pattern {
      values = ["/api/requests*"]
    }
  }
}

resource "aws_launch_template" "frontend" {
  name_prefix   = "fleetops-frontend-"
  image_id      = data.aws_ami.ubuntu_frontend.id
  instance_type = var.frontend_instance_type
  depends_on    = [aws_lb.internal]

  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_ssm.name
  }

  network_interfaces {
    security_groups             = [aws_security_group.frontend.id]
    associate_public_ip_address = false
  }

  user_data = base64encode(templatefile("${path.module}/frontend-userdata.sh", {
    internal_alb_dns = aws_lb.internal.dns_name
  }))

  key_name = var.key_name != "" ? var.key_name : null

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "fleetops-frontend"
    }
  }
}

resource "aws_autoscaling_group" "frontend" {
  name                      = "fleetops-frontend-asg"
  max_size                  = var.frontend_asg_max_size
  min_size                  = var.frontend_asg_min_size
  desired_capacity          = var.frontend_asg_desired_capacity
  vpc_zone_identifier       = aws_subnet.private[*].id
  health_check_type         = "ELB"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.frontend.id
    version = "$Latest"
  }

  target_group_arns = [aws_lb_target_group.frontend.arn]

  tag {
    key                 = "Name"
    value               = "fleetops-frontend"
    propagate_at_launch = true
  }
}

resource "aws_launch_template" "backend" {
  name_prefix   = "fleetops-backend-"
  image_id      = data.aws_ami.ubuntu_backend.id
  instance_type = var.backend_instance_type

  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_ssm.name
  }

  network_interfaces {
    security_groups             = [aws_security_group.backend.id]
    associate_public_ip_address = false
  }

  user_data = base64encode(templatefile("${path.module}/backend-userdata.sh", {
    rds_endpoint = aws_db_instance.postgres.address
    db_user      = var.db_username
    db_password  = var.db_password
    auth_seed_sql   = file("${path.module}/scripts/auth-seed.sql")
    vehicle_seed_sql = file("${path.module}/scripts/vehicle-seed.sql")
  }))

  key_name = var.key_name != "" ? var.key_name : null

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "fleetops-backend"
    }
  }
}

resource "aws_autoscaling_group" "backend" {
  name                      = "fleetops-backend-asg"
  max_size                  = var.backend_asg_max_size
  min_size                  = var.backend_asg_min_size
  desired_capacity          = var.backend_asg_desired_capacity
  vpc_zone_identifier       = aws_subnet.private[*].id
  health_check_type         = "ELB"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.backend.id
    version = "$Latest"
  }

  target_group_arns = [
    aws_lb_target_group.backend_auth.arn,
    aws_lb_target_group.backend_vehicle.arn,
    aws_lb_target_group.backend_maintenance.arn,
    aws_lb_target_group.backend_request.arn,
  ]


  tag {
    key                 = "Name"
    value               = "fleetops-backend"
    propagate_at_launch = true
  }
}

resource "aws_cloudfront_distribution" "frontend" {
  enabled = true
  aliases = var.domain_name != "" ? [var.domain_name] : []

  origin {
    domain_name = aws_lb.public.dns_name
    origin_id   = "fleetops-alb-origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = local.cert_arn != "" ? "https-only" : "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = "fleetops-alb-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD"]

    forwarded_values {
      query_string = true
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = (var.domain_name == "")
    acm_certificate_arn            = local.cert_arn != "" ? local.cert_arn : null
    ssl_support_method             = local.cert_arn != "" ? "sni-only" : null
  }

  web_acl_id = local.waf_arn != "" ? local.waf_arn : null

  tags = {
    Name = "fleetops-cloudfront"
  }
}

locals {
  cert_arn = length(aws_acm_certificate.cert) > 0 ? aws_acm_certificate.cert[0].arn : (var.certificate_arn != "" ? var.certificate_arn : "")
  waf_arn  = length(aws_wafv2_web_acl.cloudfront) > 0 ? aws_wafv2_web_acl.cloudfront[0].arn : ""
}

# ACM certificate (created in us-east-1 for CloudFront) - created only when domain_name and hosted_zone_id provided
resource "aws_acm_certificate" "cert" {
  count             = var.domain_name != "" && var.hosted_zone_id != "" ? 1 : 0
  provider          = aws.us_east_1
  domain_name       = var.domain_name
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  count   = var.domain_name != "" && var.hosted_zone_id != "" ? 1 : 0
  zone_id = var.hosted_zone_id
  name    = tolist(aws_acm_certificate.cert[0].domain_validation_options)[0].resource_record_name
  type    = tolist(aws_acm_certificate.cert[0].domain_validation_options)[0].resource_record_type
  ttl     = 60
  records = [tolist(aws_acm_certificate.cert[0].domain_validation_options)[0].resource_record_value]
}

resource "aws_acm_certificate_validation" "cert_validation" {
  count                   = var.domain_name != "" && var.hosted_zone_id != "" ? 1 : 0
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.cert[0].arn
  validation_record_fqdns = [for r in aws_route53_record.cert_validation : r.fqdn]
}

# HTTPS listener on the public ALB when a certificate is available (either created or provided)
resource "aws_lb_listener" "https" {
  count             = (var.domain_name != "" || var.certificate_arn != "") ? 1 : 0
  load_balancer_arn = aws_lb.public.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"

  certificate_arn = local.cert_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}

# WAFv2 Web ACL for CloudFront (optional)
resource "aws_wafv2_web_acl" "cloudfront" {
  count    = var.enable_waf ? 1 : 0
  provider = aws.us_east_1
  name     = "fleetops-cloudfront-waf"
  scope    = "CLOUDFRONT"

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "fleetops-waf"
    sampled_requests_enabled   = true
  }

  rule {
    name     = "AWS-AWSManagedRulesCommonRuleSet"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }
}

# Route53 record for the CloudFront distribution (alias) - optional
resource "aws_route53_record" "cloudfront_alias" {
  count   = var.domain_name != "" && var.hosted_zone_id != "" ? 1 : 0
  zone_id = var.hosted_zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = "Z2FDTNDATAQYW2"
    evaluate_target_health = false
  }
}

# RDS: subnet group, security group, and Postgres instance
resource "aws_db_subnet_group" "main" {
  name       = "fleetops-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "fleetops-db-subnet-group"
  }
}

resource "aws_security_group" "rds" {
  name        = "fleetops-rds-sg"
  description = "Allow Postgres access from backend instances"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow Postgres from backend"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.backend.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "fleetops-rds-sg"
  }
}

resource "aws_db_instance" "postgres" {
  identifier             = "fleetops-postgres"
  allocated_storage      = var.db_allocated_storage
  engine                 = "postgres"
  instance_class         = var.db_instance_class
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  kms_key_id             = aws_kms_key.rds.arn
  storage_encrypted      = true
  skip_final_snapshot    = true
  publicly_accessible    = false
  multi_az               = false

  tags = {
    Name = "fleetops-postgres"
  }
}

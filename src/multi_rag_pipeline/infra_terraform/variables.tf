variable "region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "multi-rag"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "subnet_cidr_public" {
  default = "10.0.1.0/24"
}

variable "subnet_cidr_private" {
  default = "10.0.2.0/24"
}

variable "desired_count" {
  default = 2
}

variable "api_port" {
  default = 8000
}

variable "ui_port" {
  default = 8501
}

variable "redis_port" {
  default = 6379
}


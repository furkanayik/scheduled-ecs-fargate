locals {
  service_name = "scheduled-ecs"
}

provider "aws" {
  region                  = "us-east-1"
  shared_credentials_file = "~/.aws/credentials"
}

resource "aws_default_vpc" "default" {
}

data "aws_subnet_ids" "subnets" {
  vpc_id = aws_default_vpc.default.id
}

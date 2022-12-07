terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}


resource "aws_security_group" "security_gp" {
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

data "aws_vpc" "default" {
  default = true
}


# resource "aws_instance" "proxy" {
#   ami                    = "ami-0149b2da6ceec4bb0"
#   instance_type          = "t2.large"
#   vpc_security_group_ids = [aws_security_group.security_gp.id]
#   availability_zone      = "us-east-1c"
#   tags = {
#     Name = "Proxy"
#   }
# }


resource "aws_instance" "cluster-data1" {
  ami                    = "ami-0149b2da6ceec4bb0"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.security_gp.id]
  availability_zone      = "us-east-1c"
  tags = {
    Name = "Data Node 1"
  }
  key_name = "ec2-keypair"
}

resource "aws_instance" "cluster-data2" {
  ami                    = "ami-0149b2da6ceec4bb0"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.security_gp.id]
  availability_zone      = "us-east-1c"
  tags = {
    Name = "Data Node 2"
  }
  key_name = "ec2-keypair"
}

# resource "aws_instance" "cluster-data3" {
#   ami                    = "ami-0149b2da6ceec4bb0"
#   instance_type          = "t2.micro"
#   vpc_security_group_ids = [aws_security_group.security_gp.id]
#   availability_zone      = "us-east-1c"
#   tags = {
#     Name = "Data Node 3"
#   }
#   key_name = "ec2-keypair"
# }


resource "aws_instance" "cluster-mgm" {
  ami                    = "ami-0149b2da6ceec4bb0"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.security_gp.id]
  availability_zone      = "us-east-1c"
  tags = {
    Name = "Management Node"
  }
  key_name = "ec2-keypair"
}
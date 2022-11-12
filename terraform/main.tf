terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~>4.0"
      }
    }
}

resource "aws_security_group" "everywhere" {
    name   = "everywhere"
    vpc_id = "${data.aws_vpc.default.id}"

    ingress {
        protocol    = -1
        cidr_blocks = ["0.0.0.0/0"]
        from_port   = 0
        to_port     = 0
    }
    egress {
        protocol    = -1
        cidr_blocks = ["0.0.0.0/0"]
        from_port   = 0
        to_port     = 0
    }

}

resource "aws_instance" "t2" {
    count = 1

    instance_type = "${var.t2_stand_alone}"
    key_name = "${var.key_name}"

    vpc_security_group_ids = [
        aws_security_group.everywhere.id,
    ]

    subnet_id = element(tolist(data.aws_subnets.all.ids), 1)
    user_data = "${file("${path.module}/../stand_alone.sh")}"
    ami = "ami-08c40ec9ead489470"
}
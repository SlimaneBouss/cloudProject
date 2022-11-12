// AWS specific variables
variable "aws_region" {
    description = "AWS region"
    type = string
    default = "us-east-1"
}

variable "app_name" {
    description = "Name of the application"
    default = "Cloud project final"
}

variable "api_version" {
    description = "Version of the API"
    default = "latest"
}

variable "t2_stand_alone" {
    description = "Instance type for mySQL stand alone"
    type = string
    default = "t2.micro"
}

variable "key_name" {
    description = "Name of the key pair to use"
    default = "vockey"
}

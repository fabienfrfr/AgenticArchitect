provider "aws" {
  region = "eu-west-1"
}

resource "aws_instance" "agentic_architect" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "g4dn.xlarge"
  tags = {
    Name = "AgenticArchitect"
  }
}

resource "aws_security_group" "agentic_architect_sg" {
  name        = "agentic_architect_sg"
  description = "Security group for AgenticArchitect"
  
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

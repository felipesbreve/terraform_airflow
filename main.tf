terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-04a81a99f5ec58529"
  instance_type = "t2.small"
  key_name      = "terraform"
  tags = {
    Name = "terraform"
  }
  provisioner "file" {
    source      = "job/"
    destination = "/home/ubuntu/"
  }
  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt upgrade -y",
      "sudo apt install -y python3",
      "sudo apt install -y python3-pip",
      "sudo apt install pip --upgrade pip",
      "sudo apt install -y python3-venv",
      "python3 -m venv venv",
      ". venv/bin/activate",
      "pip install -r requirements.txt",
      "python3 main.py"
    ]
  }
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("sua-chave-de-acesso-a-aws")
    host        = self.public_ip
  }
}

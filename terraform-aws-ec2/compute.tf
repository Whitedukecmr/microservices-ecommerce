resource "aws_key_pair" "deployer" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)

  tags = {
    Name = "${var.project_name}-${var.environment}-key"
  }
}

resource "aws_instance" "app_server" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  key_name                    = aws_key_pair.deployer.key_name
  associate_public_ip_address = true

  user_data = templatefile("${path.module}/user-data.sh", {
    project_name = var.project_name
  })

  root_block_device {
    volume_size           = var.root_volume_size
    volume_type           = "gp3"
    delete_on_termination = true
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-ec2"
  }
}

resource "aws_eip_association" "ec2_eip_assoc" {
  instance_id   = aws_instance.app_server.id
  allocation_id = aws_eip.ec2_eip.id
}
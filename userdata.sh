#!/bin/bash
apt update
apt install docker.io -y
apt install docker -y
apt install docker-compose -y
usermod -aG docker ubuntu
apt install git -y

cd /home/ubuntu
git clone https://github.com/liormilliger/linux-srv-data-collection.git

cd promehteus
docker-compose up -d
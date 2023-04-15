#! /bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo systemctl start docker
sudo usermod -a -G docker ec2-user
sudo systemctl enable docker
sudo curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo yum install git -y
sudo git clone https://github.com/AmirKatorza/AWS_reStart_Docker-Flask-Mongo_App.git
# wget https://github.com/AmirKatorza/AWS_reStart_Docker-Flask-Mongo_App/archive/refs/heads/master.zip
#sudo yum install unzip -y
#sudo unzip master.zip
sudo cd ./AWS_reStart_Docker-Flask-Mongo_App/
sudo echo "API_KEY_V3 = '<api_key>'" >> credentials.py
sudo docker-compose build
sudo docker-compose up
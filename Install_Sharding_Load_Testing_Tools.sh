#!/bin/bash

###################################################################################################################################
# 
# A script for Ubuntu to install useful tools for generating documents for a MongoDB cluster and generating a load on the same MongoDB cluster
# 
###################################################################################################################################

#update apt
echo "Updating apt"
sudo apt update

#install pip for python 3
echo "installing pip"
sudo apt install python3-pip -y

#install venv for python 3
echo "installing venv"
sudo apt install python3-venv -y

#install pymongo
echo "installing pymongo"
python3 -m pip install pymongo

#install git
echo "install git"
sudo apt install git -y

#changing directory
echo "installing mongo mangler in home directory"
cd ~

#fetch mongo mangler
echo "cloning mongo mangler repo"
git clone --branch add-more-pipelines https://github.com/deadsix/mongo-mangler

#cloning mongo locust repo
echo "cloning mongo locust repo"
git clone https://github.com/sabyadi/mongolocust

#create virtual environment
cd mongolocust
python3 -m venv mongolocust
source mongolocust/bin/activate

#downloading and installing mongolocust requirements
echo "installing mongo locust dependencies"
pip install -r requirements.txt

#install microk8s
echo "installing microk8s"
sudo snap install microk8s --classic

echo "Mongo Mangler, Mongo Locust, and MicroK8s are installed!"

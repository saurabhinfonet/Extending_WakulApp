#Created for COMP90055 Computing Project 
# Contribution : Ebin and Saurabh
#!/bin/bash
# setup environment
sudo apt-get update

# git setup
sudo apt-get -y install git

sudo apt-get -y install python3-pip
sudo apt-get -y install python-nltk
sudo apt-get -y install python-dev python-setuptools python-numpy python-scipy libatlas-dev
#extras for python3
sudo apt-get -y install python3-dev python3-setuptools python3-numpy python3-scipy

sudo apt-get -y install python-matplotlib
sudo apt-get -y install python3-matplotlib

sudo pip3 install -r requirements.txt

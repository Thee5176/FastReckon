#!/usr/bin/bash

pwd
# Setup script from Grepper
# Update the apt package index
sudo apt-get update

# Install packages to allow apt to use a repository over HTTPS
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker's stable repository
echo \
"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the apt package index again
sudo apt-get update

# Install the Docker dependencies
sudo apt-get install -y docker-ce docker-ce-cli docker-compose containerd.io
# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Verify Docker installation
sudo docker run hello-world


# Manage Docker user script from https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
sudo usermod -aG docker $USER

# Set instance default directory to cloned folder
echo "cd FastReckon" >> .bashrc

# Legacy: _script/setup.sh
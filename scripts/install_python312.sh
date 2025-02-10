#!/bin/bash

# Software/scripts/install_python312.sh
# install_python312.sh - Installs Python 3.12.8 and pip

# Exit on any error
set -e

echo "Installing Python 3.12.8..."

# Install prerequisites and Python 3.12
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-dev

# Install pip for Python 3.12
echo "Installing pip..."
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# Verify installations
echo "Python version:"
python3.12 --version
echo "Pip version:"
python3.12 -m pip --version

echo "Installation complete!"
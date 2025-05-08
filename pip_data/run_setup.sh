#!/bin/bash

echo "Setting up Pip environment..."

# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Python 3 and pip if not already installed
sudo apt-get install -y python3 python3-pip

# Install essential Python packages
pip3 install --upgrade pip
pip3 install \
  coqui-tts \
  sounddevice \
  pyserial \
  vosk \
  websockets \
  numpy \
  scipy

# Optional: Install virtualenv if you plan to use a venv
# pip3 install virtualenv

# Confirm audio and serial devices are available
echo "Audio devices:"
arecord -l
echo "Serial devices:"
ls /dev/tty*

echo "Setup complete. You can now run Pip using ./run_pip.sh"


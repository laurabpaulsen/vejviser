#!/bin/bash

# Get the directory of the Bash script
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

# Create a virtual environment in the same directory as the script
python -m venv "$scriptDir/env"

# Activate the virtual environment
source "$scriptDir/env/bin/activate"

# Install programs
sudo apt-get install python-poppler
sudo apt-get install poppler-utils
sudo apt-get install -y libpoppler-cpp-dev
sudo apt install tesseract-ocr -y
sudo apt-get install tesseract-ocr-dan


# Install requirements from the same directory as the script
python -m pip install -r "$scriptDir/requirements.txt"

echo "Done!"


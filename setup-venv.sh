#!/bin/bash -ex

# Re-create the virtual env
rm -fr venv
python3 -m venv venv
source venv/bin/activate
pip install wheel
# Install the required packages
pip install -r requirements.txt


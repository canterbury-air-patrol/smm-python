#!/bin/bash -ex

source venv/bin/activate

hatch fmt --check

pylint src/

flake8 src/

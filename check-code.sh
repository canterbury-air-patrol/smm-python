#!/bin/bash -ex

source venv/bin/activate

hatch fmt --check

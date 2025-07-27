#!/usr/bin/env bash
set -e
python -m pip install --upgrade pip
python -m pip install --no-index --find-links=./wheels -r requirements.txt



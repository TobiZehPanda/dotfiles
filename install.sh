#!/bin/bash

python -m venv .env && source ".env/bin/activate"
pip install --disable-pip-version-check -q -r requirements.txt
python dotfiles.py $*

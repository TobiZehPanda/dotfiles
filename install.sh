#!/bin/bash

virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

source .env/bin/activate
python tui.py

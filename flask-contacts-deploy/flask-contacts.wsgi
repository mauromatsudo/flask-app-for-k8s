#!/usr/bin/python3
import sys
proj_path = '/app'
sys.path.insert(0, proj_path)
#sys.path.insert(0, '/app/.venv/bin')

from app import app as application


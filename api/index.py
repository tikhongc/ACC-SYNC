"""
Vercel entrypoint for the Flask app.
This wraps the root-level app.py so @vercel/python can pick up a WSGI handler.
"""

import os
import sys

# Ensure project root is on the import path
api_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(api_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import app as application

# Alias commonly used by some WSGI hosts
app = application

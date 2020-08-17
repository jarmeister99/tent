#!/var/www/tent/venv/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/tent/")
sys.path.insert(0,"/var/www/tent/venv/bin")
sys.path.insert(0,"/var/www/tent/venv/lib/python3.8/site-packages")

from tent import app as application

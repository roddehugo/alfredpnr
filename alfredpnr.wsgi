import logging, sys
logging.basicConfig(stream=sys.stderr)

activate_this = '/var/www/alfredpnr.favrodd.com/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0,'/var/www/alfredpnr.favrodd.com')
from flaskpnr import app as application

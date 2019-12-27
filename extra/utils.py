import os
import uuid
import configparser
from urllib.parse import urlencode
from urllib.request import Request, urlopen

configPath = os.path.join(os.path.dirname(__file__), 'config.ini')

# @csprance snipped this bit to remove any user tracking
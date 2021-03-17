import os

debug = False
testing = False

# Discord Information
BOT_PREFIX = ('!', '+')
TOKEN = os.getenv('WADSWORTH_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
OWNERS = [322840172985188355,]
BOT_CHANNEL = 819731985780965376
BLACKLIST = []

# Current Modeules
STARTUP_COGS = [
    'cogs.office',
] 

# db Information
if testing:
    DB_LOCATION = 'test.db'
else:    
    DB_LOCATION = 'data/wadsworth.db'


# JitBit Information
HELPDESK_URL = os.getenv('JITBIT_SUPPORT_URL')
HELPDESK_USER = os.getenv('JITBIT_USER')
HELPDESK_PWD = os.getenv('JITBIT_PASSWORD')

# Constants
CONFIRMS = ["y", "yes", "yep", "yea",]
DENIES = ["n", "no", "nope",  "nah"]

# Info
VERSION = '1.0.1'
DESCRIPTION = """
Wadworth was created specifically for the Arizona Pipeline IT department to better handle communications and to streamline many repetitive tasks.
"""
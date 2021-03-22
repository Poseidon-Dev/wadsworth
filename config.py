import os, psycopg2

TESTING = False
POSTGRES = True

# Discord Information
BOT_PREFIX = ('!', '-')
TOKEN = os.getenv('BOT_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
OWNERS = os.getenv('OWNERS')
BOT_CHANNEL = int(os.getenv('BOT_CHANNEL'))
BLACKLIST = []

# Current Modeules
STARTUP_COGS = [
    'cogs.office', 'cogs.info', 'cogs.ticket', 'cogs.tasks', 'cogs.password'
] 

# db Information
DB_LOCATION = os.getenv('DB_LOCATION')
WORD_SITE = os.getenv('WORD_SITE')
def conn():
    POSTGRES_CONN = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PWD'),
        port=os.getenv('POSTGRES_PORT')
    )
    return POSTGRES_CONN


# JitBit Information
HELPDESK_URL = os.getenv('JITBIT_SUPPORT_URL')
HELPDESK_USER = os.getenv('JITBIT_USER')
HELPDESK_PWD = os.getenv('JITBIT_PASSWORD')

# Constants
CONFIRMS = ["y", "yes", "yep", "yea",]
DENIES = ["n", "no", "nope",  "nah"]

# Info
VERSION = os.getenv('VERSION')
DESCRIPTION = """
Wadworth was created specifically for the Arizona Pipeline IT department to better handle communications and to streamline many repetitive tasks.
"""

# Testing
if TESTING:
    DB_LOCATION = os.getenv('DB_TEST_LOCATION')
    TOKEN = os.getenv('BOT_TEST_TOKEN')
    STARTUP_COGS = [
    'cogs.info',
    ] 
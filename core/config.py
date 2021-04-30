import os, psycopg2
import discord
from discord.ext import commands

TESTING = False
POSTGRES = True

# BOT INFO
VERSION = os.getenv('VERSION')
DESCRIPTION = """
Wadworth was created specifically for the Arizona Pipeline IT department to better handle communications and to streamline many repetitive tasks.
"""

## DISCORD
# CHANNELS
BOT_CHANNEL = int(os.getenv('BOT_CHANNEL'))
OFFICE_CHANNEL = int(os.getenv('OFFICE_CHANNEL'))
WADSWORTH_CHANNEL = int(os.getenv('WADSWORTH_CHANNEL'))
EMAIL_CHANNEL = int(os.getenv('EMAIL_CHANNEL'))
INVENTORY_CHANNEL = int(os.getenv('INVENTORY_CHANNEL'))

# SETTINGS
BOT_PREFIX = ('!', '-')
TOKEN = os.getenv('BOT_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
OWNERS = os.getenv('OWNERS')
BLACKLIST = []
INTENTS = discord.Intents.default()
BOT = commands.Bot(BOT_PREFIX, intents=INTENTS)
BOT.remove_command('help')
CHANNEL = BOT.get_channel(BOT_CHANNEL)


# CURRENT MODULES
STARTUP_COGS = [
    'apps.info',
    'apps.office',
    'apps.password',
    'apps.censor',
    'apps.erp',
    'apps.inventory',
] 

# LOCAL DB
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


## API INTEGRATIONS
# ERP API
ERP_HOST = os.getenv('ERP_HOST')
ERP_UID = os.getenv('ERP_UID')
ERP_PWD = os.getenv('ERP_PWD')

# JITBIT API
HELPDESK_URL = os.getenv('JITBIT_SUPPORT_URL')
HELPDESK_USER = os.getenv('JITBIT_USER')
HELPDESK_PWD = os.getenv('JITBIT_PASSWORD')

# EMAIL
EMAIL_UID = os.getenv('EMAIL_UID')
EMAIL_PWD = os.getenv('EMAIL_PWD')
EMAIL_SMTP = os.getenv('EMAIL_SMTP')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT'))
EMAIL_TO = os.getenv('EMAIL_TO')

# VERIZON API

# GOOGLE API

# CONSTANTS
CONFIRMS = ["y", "yes", "yep", "yea",]
DENIES = ["n", "no", "nope",  "nah"]
SWEAR_LIST = os.getenv('SWEAR_WORDS').split()


if TESTING:
    TOKEN = os.getenv('BOT_TEST_TOKEN')
    BOT_CHANNEL = int(os.getenv('BOT_TEST_CHANNEL'))
    CHANNEL = BOT.get_channel(BOT_CHANNEL)

    # LOCAL DB
    DB_LOCATION = os.getenv('DB_TEST_LOCATION')
    def conn():
        POSTGRES_CONN = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_TEST_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PWD'),
            port=os.getenv('POSTGRES_PORT')
        )
        return POSTGRES_CONN

    # EMAIL
    EMAIL_TO = os.getenv('EMAIL_TO_TEST')

    # CURRENT MODULES
    STARTUP_COGS = [
    'apps.info',
    'apps.inventory',
    ] 

    print('=' * 8 + 'TESTING MODE' + '=' * 8 )
   


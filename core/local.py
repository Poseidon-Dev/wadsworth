import os, psycopg2
from core.config import BOT

# DISCORD
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

# CURRENT MODULES
STARTUP_COGS = [
'cogs.info', 'cogs.office', 'cogs.password', 'cogs.censor'
] 

print('=' * 8 + 'TESTING MODE' + '=' * 8 )
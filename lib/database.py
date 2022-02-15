import os

from dotenv import load_dotenv
from mysql import connector as CONN

load_dotenv()


def db_connect():
    return CONN.connect(
        host=os.environ.get('MYSQL_HOST'), user=os.environ.get('MYSQL_USER'), password=os.environ.get('MYSQL_PASSWORD'),
        database=os.environ.get('MYSQL_DB'), port=os.environ.get('MYSQL_PORT')
    )

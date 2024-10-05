import psycopg2
from . import config


def connect_postgresql():
    return psycopg2.connect(**config.POSTGRESQL_CONFIG)



def test_connection():
    try:
        if connect_postgresql():
            print("postgre connection success")
    except Exception as e:
        print(f"postgre connection FAILED with an error: {e}")

test_connection()
import psycopg2
from . import config
import time

def connect_postgresql():
    return psycopg2.connect(**config.POSTGRESQL_CONFIG)



def test_connection():
    try:
        for i in range(10):
            if connect_postgresql():
                print("postgre connection success")
                time.sleep(0.5)
                break
    except Exception as e:
        print(f"postgre connection FAILED with an error: {e}")

test_connection()
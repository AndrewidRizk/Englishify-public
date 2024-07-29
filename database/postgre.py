import psycopg2
from psycopg2 import OperationalError

def test_postgresql_connection():
    try:
        connection = psycopg2.connect(
            host="",
            database="",
            user="",
            password=""
        )
        print("PostgreSQL connection successful")
    except OperationalError as e:
        print(f"PostgreSQL connection failed: {e}")
    finally:
        if connection:
            connection.close()

# Replace with your PostgreSQL credentials
test_postgresql_connection()

# Database configuration settings
import os
host= os.environ.get('DB_HOST')
db= os.environ.get('DB_NAME') 
user= os.environ.get('DB_USER') 
password=  os.environ.get('DB_PASSWORD') 
port= os.environ.get('DB_PORT')

POSTGRESQL_CONFIG = {
    'host': host,
    'database': db,
    'user': user,
    'password': password,
    'port': port
}


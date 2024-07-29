from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import logging
def elasticsearch_con():
    # Enable logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("elasticsearch").setLevel(logging.DEBUG)

    # Define the connection details
    host = ""
    port = 
    username = ""
    password = ""

    # Create an Elasticsearch client
    es = Elasticsearch(
        [f"https://{host}:{port}"],
        basic_auth=(username, password),
        verify_certs=False
    )

    # Check if the client is connected
    try:
        # Attempt to ping the Elasticsearch server
        if es.ping():
            print("Connected to Elasticsearch!")
        else:
            print("Could not connect to Elasticsearch.")
    except ConnectionError as e:
        print(f"Connection Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Optionally, you can try to get some basic information from the cluster
elasticsearch_con()
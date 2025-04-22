import os
import pymongo
from pymongo.errors import ConnectionFailure

MONGO_URI = os.getenv("MONGO_URI")

def test_mongo_connection():
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

        client.server_info()  # Will attempt to connect to the server

        print("Connection Success.")
    except ConnectionFailure as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_mongo_connection()

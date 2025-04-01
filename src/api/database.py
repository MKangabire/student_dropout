from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import pandas as pd

# Encode special characters in the password
username = "mkangabire"
password = quote_plus("Correction@1")  # Encodes "@" to "%40"

# Construct the MongoDB URI
uri = f"mongodb+srv://{username}:{password}@cluster0.xttbywk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_mongo_client():
    """
    Returns a MongoDB client instance.
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

def save_to_mongo(df, collection_name):
    """
    Saves a DataFrame to a specified MongoDB collection in Student_dropout_db.
    
    Args:
        df: DataFrame to save.
        collection_name: Name of the collection ('train' or 'test').
    """
    client = get_mongo_client()
    db = client["Student_dropout_db"]  # Use the existing database name with capital 'S'
    collection = db[collection_name]
    collection.delete_many({})  # Clear existing data in the collection
    data = df.to_dict(orient="records")
    collection.insert_many(data)
    client.close()

def fetch_from_mongo(collection_name):
    """
    Fetches data from a MongoDB collection and returns it as a DataFrame.
    
    Args:
        collection_name: Name of the collection ('train' or 'test').
    
    Returns:
        DataFrame with the collection data, or None if fetch fails.
    """
    try:
        client = get_mongo_client()
        db = client["Student_dropout_db"]  # Use the existing database name with capital 'S'
        collection = db[collection_name]
        data = list(collection.find({}, {"_id": 0}))  # Exclude '_id' field
        client.close()
        if not data:
            return None
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Failed to fetch from MongoDB collection '{collection_name}': {e}")
        return None
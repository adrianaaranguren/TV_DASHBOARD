from pymongo import MongoClient
import json
from datetime import datetime

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def sample_collection_data():
    """Sample data from collections to understand structure"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        
        print("Available collections:")
        collections = db.list_collection_names()
        for collection in collections:
            print(f"- {collection}")
        
        print("\n" + "="*50)
        
        # Sample calls collection
        print("SAMPLING CALLS COLLECTION:")
        calls_collection = db.calls
        sample_call = calls_collection.find_one()
        if sample_call:
            print("Sample call document:")
            print(json.dumps(sample_call, default=str, indent=2))
        else:
            print("No calls found or collection doesn't exist")
        
        print("\n" + "="*50)
        
        # Sample deals collection
        print("SAMPLING DEALS COLLECTION:")
        deals_collection = db.deals
        sample_deal = deals_collection.find_one()
        if sample_deal:
            print("Sample deal document:")
            print(json.dumps(sample_deal, default=str, indent=2))
        else:
            print("No deals found or collection doesn't exist")
        
        print("\n" + "="*50)
        
        # Get unique user IDs from calls
        print("UNIQUE USER IDs FROM CALLS:")
        if sample_call:
            pipeline = [
                {"$group": {"_id": "$ownerId"}},
                {"$limit": 10}
            ]
            user_ids = list(calls_collection.aggregate(pipeline))
            for user in user_ids:
                print(f"- {user['_id']}")
        
        print("\n" + "="*50)
        
        # Get unique user IDs from deals
        print("UNIQUE USER IDs FROM DEALS:")
        if sample_deal:
            pipeline = [
                {"$group": {"_id": "$createdById"}},
                {"$limit": 10}
            ]
            user_ids = list(deals_collection.aggregate(pipeline))
            for user in user_ids:
                print(f"- {user['_id']}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sample_collection_data() 
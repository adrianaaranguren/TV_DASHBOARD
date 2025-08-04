from pymongo import MongoClient
import json

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def get_unique_user_ids():
    """Get all unique user IDs from calls and deals collections"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        
        # Get unique user IDs from calls
        calls_collection = db.calls
        call_user_ids = set()
        pipeline_calls = [
            {"$group": {"_id": "$ownerId"}},
            {"$match": {"_id": {"$ne": None}}}
        ]
        call_results = list(calls_collection.aggregate(pipeline_calls))
        for result in call_results:
            call_user_ids.add(str(result["_id"]))
        
        # Get unique user IDs from deals
        deals_collection = db.deals
        deal_user_ids = set()
        pipeline_deals = [
            {"$group": {"_id": "$ownerId"}},
            {"$match": {"_id": {"$ne": None}}}
        ]
        deal_results = list(deals_collection.aggregate(pipeline_deals))
        for result in deal_results:
            deal_user_ids.add(str(result["_id"]))
        
        # Combine all user IDs
        all_user_ids = call_user_ids.union(deal_user_ids)
        
        print("All unique user IDs found:")
        print("=" * 50)
        for user_id in sorted(all_user_ids):
            print(f'"{user_id}": "USER_NAME_HERE",')
        
        print("\n" + "=" * 50)
        print(f"Total unique user IDs: {len(all_user_ids)}")
        
        client.close()
        
        return all_user_ids
        
    except Exception as e:
        print(f"Error: {e}")
        return set()

if __name__ == "__main__":
    get_unique_user_ids() 
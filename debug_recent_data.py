from pymongo import MongoClient
from datetime import datetime, timedelta
import json

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def debug_recent_data():
    """Debug recent data from last 30 days"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        
        # Get date ranges for last 30 days
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        print(f"Looking for data from: {thirty_days_ago} to {today}")
        print("=" * 60)
        
        # Check calls collection
        calls_collection = db.calls
        print("CALLS COLLECTION - LAST 30 DAYS:")
        print("-" * 40)
        
        # Find recent calls
        recent_calls = list(calls_collection.find({
            "createdAt": {
                "$gte": thirty_days_ago,
                "$lte": today
            }
        }).sort("createdAt", -1).limit(10))
        
        print(f"Recent calls found: {len(recent_calls)}")
        for i, call in enumerate(recent_calls):
            print(f"  {i+1}. {call.get('createdAt')} - Owner: {call.get('ownerId')}")
        
        # Check deals collection
        deals_collection = db.deals
        print("\nDEALS COLLECTION - LAST 30 DAYS:")
        print("-" * 40)
        
        # Find recent deals
        recent_deals = list(deals_collection.find({
            "properties.createdate": {
                "$gte": thirty_days_ago.isoformat() + "Z",
                "$lte": today.isoformat() + "Z"
            }
        }).sort("properties.createdate", -1).limit(10))
        
        print(f"Recent deals found: {len(recent_deals)}")
        for i, deal in enumerate(recent_deals):
            print(f"  {i+1}. {deal.get('properties', {}).get('createdate')} - Owner: {deal.get('ownerId')}")
        
        # Check for any data in the last 6 months
        six_months_ago = today - timedelta(days=180)
        print(f"\nCHECKING LAST 6 MONTHS ({six_months_ago} to {today}):")
        print("-" * 50)
        
        # Calls in last 6 months
        calls_6m = list(calls_collection.find({
            "createdAt": {
                "$gte": six_months_ago,
                "$lte": today
            }
        }))
        print(f"Calls in last 6 months: {len(calls_6m)}")
        
        # Deals in last 6 months
        deals_6m = list(deals_collection.find({
            "properties.createdate": {
                "$gte": six_months_ago.isoformat() + "Z",
                "$lte": today.isoformat() + "Z"
            }
        }))
        print(f"Deals in last 6 months: {len(deals_6m)}")
        
        # Show some sample dates from the data
        print(f"\nSAMPLE DATES FROM DATA:")
        print("-" * 30)
        
        # Sample call dates
        sample_calls = list(calls_collection.find().sort("createdAt", -1).limit(5))
        print("Recent call dates:")
        for call in sample_calls:
            print(f"  {call.get('createdAt')}")
        
        # Sample deal dates
        sample_deals = list(deals_collection.find().sort("properties.createdate", -1).limit(5))
        print("\nRecent deal dates:")
        for deal in sample_deals:
            print(f"  {deal.get('properties', {}).get('createdate')}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_recent_data() 
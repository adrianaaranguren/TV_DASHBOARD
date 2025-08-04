from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def debug_calls():
    """Debug call data to see what's available"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        calls_collection = db.calls
        
        # Get current week dates
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        print(f"Current week: {start_of_week} to {end_of_week}")
        print("=" * 60)
        
        # Check total calls in database
        total_calls = calls_collection.count_documents({})
        print(f"Total calls in database: {total_calls}")
        
        # Check calls in current week
        week_calls = list(calls_collection.find({
            "createdAt": {
                "$gte": start_of_week,
                "$lte": end_of_week
            }
        }))
        print(f"Calls in current week: {len(week_calls)}")
        
        # Check calls in last 30 days
        thirty_days_ago = today - timedelta(days=30)
        recent_calls = list(calls_collection.find({
            "createdAt": {
                "$gte": thirty_days_ago,
                "$lte": today
            }
        }))
        print(f"Calls in last 30 days: {len(recent_calls)}")
        
        # Show sample call dates
        print(f"\nSAMPLE CALL DATES:")
        print("-" * 30)
        sample_calls = list(calls_collection.find().sort("createdAt", -1).limit(10))
        for i, call in enumerate(sample_calls):
            print(f"  {i+1}. {call.get('createdAt')} - Owner: {call.get('ownerId')} - HubSpot Owner: {call.get('hubspotData', {}).get('properties', {}).get('hubspot_owner_id')}")
        
        # Test the hubspot_owner_id field
        print(f"\nTESTING HUBSPOT OWNER ID FIELD:")
        print("-" * 40)
        calls_with_hubspot_owner = list(calls_collection.find({
            "hubspotData.properties.hubspot_owner_id": {"$exists": True, "$ne": None}
        }).limit(5))
        
        print(f"Calls with hubspot_owner_id: {len(calls_with_hubspot_owner)}")
        for i, call in enumerate(calls_with_hubspot_owner):
            hubspot_owner = call.get('hubspotData', {}).get('properties', {}).get('hubspot_owner_id')
            owner_id = call.get('ownerId')
            print(f"  {i+1}. HubSpot Owner: {hubspot_owner}, Owner ID: {owner_id}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_calls() 
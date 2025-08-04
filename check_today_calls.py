from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def check_today_calls():
    """Check for calls from today (August 4th, 2025)"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        calls_collection = db.calls
        
        # Check for calls from today (August 4th, 2025)
        today = datetime(2025, 8, 4)  # August 4th, 2025
        start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        print(f"Checking for calls on: {start_of_day} to {end_of_day}")
        print("=" * 60)
        
        # Check calls from today
        today_calls = list(calls_collection.find({
            "createdAt": {
                "$gte": start_of_day,
                "$lte": end_of_day
            }
        }))
        
        print(f"Calls from today (August 4th): {len(today_calls)}")
        
        if today_calls:
            print("\nSAMPLE CALLS FROM TODAY:")
            print("-" * 30)
            for i, call in enumerate(today_calls[:5]):
                print(f"  {i+1}. {call.get('createdAt')} - Owner: {call.get('ownerId')} - HubSpot Owner: {call.get('hubspotData', {}).get('properties', {}).get('hubspot_owner_id')}")
        
        # Check for calls from the last few days
        print(f"\nCHECKING LAST 7 DAYS:")
        print("-" * 20)
        for i in range(7):
            check_date = today - timedelta(days=i)
            start_check = check_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_check = check_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            day_calls = list(calls_collection.find({
                "createdAt": {
                    "$gte": start_check,
                    "$lte": end_check
                }
            }))
            
            print(f"  {check_date.strftime('%Y-%m-%d')}: {len(day_calls)} calls")
        
        # Check most recent calls
        print(f"\nMOST RECENT CALLS:")
        print("-" * 20)
        recent_calls = list(calls_collection.find().sort("createdAt", -1).limit(10))
        for i, call in enumerate(recent_calls):
            print(f"  {i+1}. {call.get('createdAt')} - Owner: {call.get('ownerId')}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_today_calls() 
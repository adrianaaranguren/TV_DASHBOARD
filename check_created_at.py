from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def check_created_at():
    """Check the createdAt field structure"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        calls_collection = db.calls
        
        # Get a few sample calls to see the createdAt field
        sample_calls = list(calls_collection.find().limit(3))
        
        print("CHECKING CREATEDAT FIELD:")
        print("=" * 50)
        
        for i, call in enumerate(sample_calls):
            print(f"\nCall {i+1}:")
            print(f"  createdAt: {call.get('createdAt')} (type: {type(call.get('createdAt'))})")
            print(f"  ownerId: {call.get('ownerId')}")
            print(f"  hubspotData.properties.hubspot_owner_id: {call.get('hubspotData', {}).get('properties', {}).get('hubspot_owner_id')}")
        
        # Check for calls from today using createdAt
        today = datetime.now()
        start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        print(f"\nCHECKING FOR CALLS FROM TODAY ({start_of_day} to {end_of_day}):")
        print("-" * 60)
        
        today_calls = list(calls_collection.find({
            "createdAt": {
                "$gte": start_of_day,
                "$lte": end_of_day
            }
        }))
        
        print(f"Calls from today using createdAt: {len(today_calls)}")
        
        if today_calls:
            print("\nSAMPLE CALLS FROM TODAY:")
            for i, call in enumerate(today_calls[:5]):
                print(f"  {i+1}. {call.get('createdAt')} - Owner: {call.get('ownerId')}")
        
        # Check for calls from the last few days
        print(f"\nCHECKING LAST 5 DAYS:")
        print("-" * 20)
        for i in range(5):
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
        
        # Check if there are any calls with different date fields
        print(f"\nCHECKING FOR OTHER DATE FIELDS:")
        print("-" * 30)
        sample_call = sample_calls[0] if sample_calls else {}
        for key, value in sample_call.items():
            if 'date' in key.lower() or 'time' in key.lower() or 'created' in key.lower():
                print(f"  {key}: {value}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_created_at() 
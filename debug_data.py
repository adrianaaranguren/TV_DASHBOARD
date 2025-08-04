from pymongo import MongoClient
from datetime import datetime, timedelta
import json

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def debug_data():
    """Debug the data structure and queries"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        
        # Get current week and month dates
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        print(f"Current week: {start_of_week} to {end_of_week}")
        print(f"Current month: {start_of_month} to {end_of_month}")
        print("=" * 60)
        
        # Check calls collection
        calls_collection = db.calls
        print("CALLS COLLECTION DEBUG:")
        print("-" * 30)
        
        # Sample a few calls to see the date format
        sample_calls = list(calls_collection.find().limit(3))
        for i, call in enumerate(sample_calls):
            print(f"Call {i+1}:")
            print(f"  createdAt: {call.get('createdAt')} (type: {type(call.get('createdAt'))})")
            print(f"  ownerId: {call.get('ownerId')}")
            print()
        
        # Check how many calls are in current week
        week_calls = list(calls_collection.find({
            "createdAt": {
                "$gte": start_of_week,
                "$lte": end_of_week
            }
        }))
        print(f"Calls in current week: {len(week_calls)}")
        
        # Check deals collection
        deals_collection = db.deals
        print("\nDEALS COLLECTION DEBUG:")
        print("-" * 30)
        
        # Sample a few deals to see the date format
        sample_deals = list(deals_collection.find().limit(3))
        for i, deal in enumerate(sample_deals):
            print(f"Deal {i+1}:")
            print(f"  properties.createdate: {deal.get('properties', {}).get('createdate')}")
            print(f"  ownerId: {deal.get('ownerId')}")
            if 'stageHistory' in deal:
                print(f"  stageHistory: {len(deal['stageHistory'])} entries")
                for stage in deal['stageHistory'][:2]:  # Show first 2 stages
                    print(f"    - {stage.get('value')} at {stage.get('timestamp')}")
            print()
        
        # Check how many deals are in current month
        month_deals = list(deals_collection.find({
            "properties.createdate": {
                "$gte": start_of_month,
                "$lte": end_of_month
            }
        }))
        print(f"Deals in current month: {len(month_deals)}")
        
        # Test the actual aggregation pipeline
        print("\nTESTING AGGREGATION PIPELINES:")
        print("-" * 30)
        
        # Test calls aggregation
        pipeline_calls = [
            {
                "$match": {
                    "createdAt": {
                        "$gte": start_of_week,
                        "$lte": end_of_week
                    },
                    "ownerId": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$ownerId",
                    "call_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"call_count": -1}
            },
            {
                "$limit": 5
            }
        ]
        
        top_callers = list(calls_collection.aggregate(pipeline_calls))
        print(f"Top callers result: {len(top_callers)}")
        for caller in top_callers:
            print(f"  {caller['_id']}: {caller['call_count']} calls")
        
        # Test deals aggregation
        pipeline_deals = [
            {
                "$match": {
                    "properties.createdate": {
                        "$gte": start_of_week,
                        "$lte": end_of_week
                    },
                    "ownerId": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$ownerId",
                    "deal_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"deal_count": -1}
            },
            {
                "$limit": 5
            }
        ]
        
        top_bookers = list(deals_collection.aggregate(pipeline_deals))
        print(f"\nTop bookers result: {len(top_bookers)}")
        for booker in top_bookers:
            print(f"  {booker['_id']}: {booker['deal_count']} deals")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_data() 
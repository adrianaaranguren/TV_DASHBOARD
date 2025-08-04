from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def check_stage_names():
    """Check what stage names are used in the deals collection"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        deals_collection = db.deals
        
        # Get current month dates
        today = datetime.now()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        print(f"Checking stages for: {start_of_month} to {end_of_month}")
        print("=" * 60)
        
        # Get all unique stage names from recent deals
        pipeline = [
            {
                "$match": {
                    "properties.createdate": {
                        "$gte": start_of_month.isoformat() + "Z",
                        "$lte": end_of_month.isoformat() + "Z"
                    }
                }
            },
            {
                "$unwind": "$stageHistory"
            },
            {
                "$group": {
                    "_id": "$stageHistory.value",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            }
        ]
        
        stage_counts = list(deals_collection.aggregate(pipeline))
        
        print("STAGE NAMES IN CURRENT MONTH:")
        print("-" * 40)
        for stage in stage_counts:
            print(f"  {stage['_id']}: {stage['count']} times")
        
        # Check for any stage names containing "disco"
        print(f"\nSTAGES CONTAINING 'DISCO':")
        print("-" * 30)
        disco_stages = [s for s in stage_counts if 'disco' in str(s['_id']).lower()]
        for stage in disco_stages:
            print(f"  {stage['_id']}: {stage['count']} times")
        
        # Check total deals in current month
        total_deals = deals_collection.count_documents({
            "properties.createdate": {
                "$gte": start_of_month.isoformat() + "Z",
                "$lte": end_of_month.isoformat() + "Z"
            }
        })
        
        print(f"\nTOTAL DEALS IN CURRENT MONTH: {total_deals}")
        
        # Show some sample deals with their stages
        print(f"\nSAMPLE DEALS WITH STAGES:")
        print("-" * 30)
        sample_deals = list(deals_collection.find({
            "properties.createdate": {
                "$gte": start_of_month.isoformat() + "Z",
                "$lte": end_of_month.isoformat() + "Z"
            }
        }).limit(5))
        
        for i, deal in enumerate(sample_deals):
            properties = deal.get('properties', {})
            print(f"\nDeal {i+1}: {properties.get('dealname')}")
            print(f"  Created: {properties.get('createdate')}")
            print(f"  Current stage: {properties.get('dealstage')}")
            
            stage_history = deal.get('stageHistory', [])
            if stage_history:
                print("  Stage history:")
                for stage in stage_history:
                    print(f"    - {stage.get('value')} at {stage.get('timestamp')}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_stage_names() 
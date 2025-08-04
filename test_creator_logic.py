from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def test_creator_logic():
    """Test which stage history entry represents the deal creator"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        deals_collection = db.deals
        
        # Get recent deals
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        recent_deals = list(deals_collection.find({
            "properties.createdate": {
                "$gte": thirty_days_ago.isoformat() + "Z",
                "$lte": today.isoformat() + "Z"
            },
            "stageHistory": {"$exists": True, "$ne": []}
        }).limit(5))
        
        print("TESTING CREATOR LOGIC:")
        print("=" * 50)
        
        for i, deal in enumerate(recent_deals):
            print(f"\nDeal {i+1}: {deal.get('properties', {}).get('dealname')}")
            print(f"  Created: {deal.get('properties', {}).get('createdate')}")
            print(f"  Owner: {deal.get('ownerId')}")
            
            stage_history = deal.get('stageHistory', [])
            if stage_history:
                print("  Stage History:")
                for j, stage in enumerate(stage_history):
                    print(f"    {j+1}. {stage.get('value')} at {stage.get('timestamp')} by {stage.get('updatedByUserId')}")
                
                # Test both approaches
                first_creator = stage_history[0].get('updatedByUserId') if stage_history else None
                last_creator = stage_history[-1].get('updatedByUserId') if stage_history else None
                
                print(f"  First stage creator: {first_creator}")
                print(f"  Last stage creator: {last_creator}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_creator_logic() 
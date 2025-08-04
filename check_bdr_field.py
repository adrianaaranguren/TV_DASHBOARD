from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def check_bdr_field():
    """Check if the 'bdr' field represents the deal creator"""
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
            }
        }).limit(10))
        
        print("ANALYZING 'BDR' FIELD:")
        print("=" * 50)
        
        for i, deal in enumerate(recent_deals):
            properties = deal.get('properties', {})
            print(f"\nDeal {i+1}: {properties.get('dealname')}")
            print(f"  Created: {properties.get('createdate')}")
            print(f"  Owner ID: {deal.get('ownerId')}")
            print(f"  HubSpot Owner ID: {properties.get('hubspot_owner_id')}")
            print(f"  BDR: {properties.get('bdr')}")
            
            # Check stage history
            stage_history = deal.get('stageHistory', [])
            if stage_history:
                print(f"  First stage by: {stage_history[0].get('updatedByUserId')}")
                print(f"  Last stage by: {stage_history[-1].get('updatedByUserId')}")
        
        # Check how many deals have BDR field populated
        total_recent = len(recent_deals)
        deals_with_bdr = len([d for d in recent_deals if d.get('properties', {}).get('bdr')])
        
        print(f"\n" + "=" * 50)
        print(f"STATISTICS:")
        print(f"  Total recent deals: {total_recent}")
        print(f"  Deals with BDR field: {deals_with_bdr}")
        print(f"  BDR field populated: {deals_with_bdr/total_recent*100:.1f}%")
        
        # Check unique BDR values
        bdr_values = set()
        for deal in recent_deals:
            bdr = deal.get('properties', {}).get('bdr')
            if bdr:
                bdr_values.add(bdr)
        
        print(f"  Unique BDR values: {len(bdr_values)}")
        print(f"  BDR values: {sorted(bdr_values)}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_bdr_field() 
from pymongo import MongoClient
import json

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def check_deal_creator_fields():
    """Check what fields are available for deal creators"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        deals_collection = db.deals
        
        # Get a few sample deals to see the structure
        sample_deals = list(deals_collection.find().limit(3))
        
        print("DEAL STRUCTURE ANALYSIS:")
        print("=" * 50)
        
        for i, deal in enumerate(sample_deals):
            print(f"\nDeal {i+1}:")
            print(f"  _id: {deal.get('_id')}")
            print(f"  dealId: {deal.get('dealId')}")
            print(f"  ownerId: {deal.get('ownerId')}")
            
            # Check properties
            properties = deal.get('properties', {})
            print(f"  properties.hubspot_owner_id: {properties.get('hubspot_owner_id')}")
            print(f"  properties.createdate: {properties.get('createdate')}")
            print(f"  properties.dealname: {properties.get('dealname')}")
            
            # Show ALL properties to find creator fields
            print("  ALL properties:")
            for key, value in properties.items():
                print(f"    - {key}: {value}")
            
            # Check stageHistory for any creator info
            if 'stageHistory' in deal:
                print("  Stage History:")
                for stage in deal['stageHistory']:
                    print(f"    - {stage.get('value')} at {stage.get('timestamp')} by {stage.get('updatedByUserId')}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_deal_creator_fields() 
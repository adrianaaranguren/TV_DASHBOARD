from pymongo import MongoClient
import json
from datetime import datetime, timedelta

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

def show_sample_deal():
    """Show a complete sample deal document"""
    try:
        client = MongoClient(ALL_DATA_MONGO_URI)
        db = client[ALL_DATA_DB_NAME]
        deals_collection = db.deals
        
        # Get a recent deal
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        sample_deal = deals_collection.find_one({
            "properties.createdate": {
                "$gte": thirty_days_ago.isoformat() + "Z",
                "$lte": today.isoformat() + "Z"
            }
        })
        
        if not sample_deal:
            # If no recent deals, get any deal
            sample_deal = deals_collection.find_one()
        
        print("COMPLETE SAMPLE DEAL DOCUMENT:")
        print("=" * 60)
        print(json.dumps(sample_deal, default=str, indent=2))
        
        print("\n" + "=" * 60)
        print("PROPERTIES ANALYSIS:")
        print("=" * 60)
        
        if sample_deal:
            properties = sample_deal.get('properties', {})
            print(f"Total properties: {len(properties)}")
            print("\nAll property keys:")
            for key in sorted(properties.keys()):
                value = properties[key]
                print(f"  - {key}: {value}")
            
            print(f"\nTop-level fields:")
            for key, value in sample_deal.items():
                if key != 'properties':
                    print(f"  - {key}: {value}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    show_sample_deal() 
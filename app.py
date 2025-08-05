from flask import Flask, render_template
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB connection
ALL_DATA_MONGO_URI = "mongodb+srv://justin:1Z8p5OEc4npjch6g@cariina-internal-databa.b6us4bb.mongodb.net/cariina-internal?retryWrites=true&w=majority&appName=cariina-internal-database"
ALL_DATA_DB_NAME = "cariina-internal"

# User ID to name mapping dictionary
# You can fill this in with the actual names
USER_ID_TO_NAME = {
    "117077412": "Unknown User",
    "1238425359": "Unknown User",
    "1319489862": "Fran",
    "134977294": "Unknown User",
    "161339161": "Unknown User",
    "184854685": "Tobey",
    "2050192952": "Ailish",
    "67047645": "Ailish",
    "271795639": "JP",
    "387992756": "Nick",
    "609638562": "Rhett",
    "690375200": "Eliza",
    "725081258": "Jack",
    "73624705": "Matt",
    "73625515": "Unknown User",
    "76003234": "Madyson",
    "76003327": "Myles",
    "76299624": "Katie",
    "76749881": "Michael",
    "77014297": "Nevin",
    "77762570": "Abby",
    "79017963": "Youssef",
    "79052085": "Jack",
    "79784775": "Pete",
    "80447308": "Jess",
    "80563502": "Kory",
    "80566617": "Owen",
    "80740888": "Pat",
    "80920342": "Ava",
    "80924094": "Gaetan",
    "83057731": "Unknown User",
    "81971802": "PJ",
    "69764725": "Fran"
}

def get_mongo_client():
    """Get MongoDB client"""
    return MongoClient(ALL_DATA_MONGO_URI)

def get_current_week_dates():
    """Get start and end dates for current week (Monday to Sunday)"""
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return start_of_week, end_of_week

def get_current_month_dates():
    """Get start and end dates for current month"""
    today = datetime.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_of_month, end_of_month

def get_last_30_days_dates():
    """Get start and end dates for last 30 days"""
    today = datetime.now()
    start_30_days_ago = today - timedelta(days=30)
    start_30_days_ago = start_30_days_ago.replace(hour=0, minute=0, second=0, microsecond=0)
    end_today = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_30_days_ago, end_today

@app.route('/')
def dashboard():
    try:
        client = get_mongo_client()
        db = client[ALL_DATA_DB_NAME]
        
        # Get date ranges
        week_start, week_end = get_current_week_dates()
        month_start, month_end = get_current_month_dates()
        
        # Top 5 callers this month
        calls_collection = db.calls
        pipeline_calls = [
            {
                "$match": {
                    "hubspotData.properties.hs_createdate": {
                        "$gte": month_start.isoformat() + "Z",
                        "$lte": month_end.isoformat() + "Z"
                    },
                    "hubspotData.properties.hubspot_owner_id": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$hubspotData.properties.hubspot_owner_id",
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
        
        # Top 5 bookers this month
        deals_collection = db.deals
        pipeline_bookers = [
            {
                "$match": {
                    "properties.createdate": {
                        "$gte": month_start.isoformat() + "Z",
                        "$lte": month_end.isoformat() + "Z"
                    },
                    "stageHistory": {"$exists": True, "$ne": []}
                }
            },
            {
                "$addFields": {
                    "creatorId": {
                        "$substr": [
                            {"$arrayElemAt": ["$stageHistory.sourceId", -1]},
                            7,
                            -1
                        ]
                    }
                }
            },
            {
                "$match": {
                    "creatorId": {"$ne": None, "$ne": ""}
                }
            },
            {
                "$group": {
                    "_id": "$creatorId",
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
        
        top_bookers = list(deals_collection.aggregate(pipeline_bookers))
        
        # Top 5 reps by discos held this month
        pipeline_discos_held_reps = [
            {
                "$match": {
                    "stageHistory": {
                        "$elemMatch": {
                            "value": "16012239",
                            "timestamp": {
                                "$gte": month_start,
                                "$lte": month_end
                            }
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "creatorId": {
                        "$substr": [
                            {"$arrayElemAt": ["$stageHistory.sourceId", -1]},
                            7,
                            -1
                        ]
                    }
                }
            },
            {
                "$match": {
                    "creatorId": {"$ne": None, "$ne": ""}
                }
            },
            {
                "$group": {
                    "_id": "$creatorId",
                    "disco_held_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"disco_held_count": -1}
            },
            {
                "$limit": 5
            }
        ]
        
        top_discos_held_reps = list(deals_collection.aggregate(pipeline_discos_held_reps))
        
        # Discos scheduled this month (deals that entered presentationscheduled stage this month)
        discos_scheduled_pipeline = [
            {
                "$match": {
                    "stageHistory": {
                        "$elemMatch": {
                            "value": "presentationscheduled",
                            "timestamp": {
                                "$gte": month_start,
                                "$lte": month_end
                            }
                        }
                    }
                }
            },
            {
                "$count": "total"
            }
        ]
        
        discos_scheduled_result = list(deals_collection.aggregate(discos_scheduled_pipeline))
        discos_scheduled_count = discos_scheduled_result[0]["total"] if discos_scheduled_result else 0
        
        # Discos held this month
        discos_held_pipeline = [
            {
                "$match": {
                    "stageHistory": {
                        "$elemMatch": {
                            "value": "16012239",
                            "timestamp": {
                                "$gte": month_start,
                                "$lte": month_end
                            }
                        }
                    }
                }
            },
            {
                "$count": "total"
            }
        ]
        
        discos_held_result = list(deals_collection.aggregate(discos_held_pipeline))
        discos_held_count = discos_held_result[0]["total"] if discos_held_result else 0
        
        # Deals closed this month
        deals_closed_pipeline = [
            {
                "$match": {
                    "stageHistory": {
                        "$elemMatch": {
                            "value": "closedwon",
                            "timestamp": {
                                "$gte": month_start,
                                "$lte": month_end
                            }
                        }
                    }
                }
            },
            {
                "$count": "total"
            }
        ]
        
        deals_closed_result = list(deals_collection.aggregate(deals_closed_pipeline))
        deals_closed_count = deals_closed_result[0]["total"] if deals_closed_result else 0
        
        # Format data for template
        top_callers_formatted = []
        for caller in top_callers:
            user_id = str(caller["_id"])  # Convert to string to ensure matching
            name = USER_ID_TO_NAME.get(user_id, f"User {user_id}")
            top_callers_formatted.append({
                "name": name,
                "count": caller["call_count"]
            })
        
        top_bookers_formatted = []
        for booker in top_bookers:
            user_id = booker["_id"]
            name = USER_ID_TO_NAME.get(user_id, f"User {user_id}")
            top_bookers_formatted.append({
                "name": name,
                "count": booker["deal_count"]
            })
        
        top_discos_held_reps_formatted = []
        for rep in top_discos_held_reps:
            user_id = rep["_id"]
            name = USER_ID_TO_NAME.get(user_id, f"User {user_id}")
            top_discos_held_reps_formatted.append({
                "name": name,
                "count": rep["disco_held_count"]
            })
        
        client.close()
        
        # Goal values (you can adjust these as needed)
        discos_scheduled_goal = 210
        discos_held_goal = 170
        deals_closed_goal = 20
        
        return render_template('dashboard.html',
                             top_callers=top_callers_formatted,
                             top_bookers=top_bookers_formatted,
                             top_discos_held_reps=top_discos_held_reps_formatted,
                             discos_scheduled=discos_scheduled_count,
                             discos_held=discos_held_count,
                             deals_closed=deals_closed_count,
                             discos_scheduled_goal=discos_scheduled_goal,
                             discos_held_goal=discos_held_goal,
                             deals_closed_goal=deals_closed_goal,
                             current_week=f"{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}",
                             current_month=month_start.strftime('%B %Y'))
    
    except Exception as e:
        print(f"Error: {e}")
        return render_template('dashboard.html',
                             top_callers=[],
                             top_bookers=[],
                             top_discos_held_reps=[],
                             discos_scheduled=0,
                             discos_held=0,
                             deals_closed=0,
                             discos_scheduled_goal=210,
                             discos_held_goal=170,
                             deals_closed_goal=20,
                             current_week="Error",
                             current_month="Error",
                             error=str(e))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port) 
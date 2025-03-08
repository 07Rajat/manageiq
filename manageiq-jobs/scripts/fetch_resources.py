# import pymongo
# import sys
# import json

# def fetch_resources(db_name, team_name, mongodb_uri):
#     try:
#         # Connect to MongoDB
#         client = pymongo.MongoClient(mongodb_uri)
#         db = client[db_name]
        
#         # Use the team name as the collection name (dynamic)
#         collection = db[team_name]

#         # Fetch allocated resources for the team
#         team_data = collection.find_one({}) 

#         if team_data:
#             allocated_cpu = team_data.get("Allocated_CPU")
#             allocated_memory_gb = team_data.get("Allocated_Memory")

#             if allocated_cpu is None or allocated_memory_gb is None:
#                 return {"error": "Required fields missing in MongoDB document"}

#             return {
#                 "allocated_cpu": allocated_cpu,
#                 "allocated_memory_gb": allocated_memory_gb
#             }
#         else:
#             return {"error": f"No data found for {team_name} in the collection."}

#     except Exception as e:
#         return {"error": f"Failed to fetch data from MongoDB: {str(e)}"}

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print(json.dumps({"error": "Usage: python3 fetch_resources.py <db_name> <team_name> <mongodb_uri>"}))
#         sys.exit(1)

#     db_name = sys.argv[1]
#     team_name = sys.argv[2]
#     mongodb_uri = sys.argv[3]

#     result = fetch_resources(db_name, team_name, mongodb_uri)

#     print(json.dumps(result))

import pymongo
import sys
import json

def fetch_resources(db_name, team_name, mongodb_uri):
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongodb_uri)
        db = client[db_name]
        
        # Use the team name as the collection name (dynamic)
        collection = db[team_name]

        # Fetch allocated resources for the team
        team_data = collection.find_one({}) 

        if team_data:
            allocated_cpu = team_data.get("Allocated_CPU")
            allocated_memory_gb = team_data.get("Allocated_Memory")

            if allocated_cpu is None or allocated_memory_gb is None:
                return {"error": "Required fields missing in MongoDB document"}

            return {
                "allocated_cpu": allocated_cpu,
                "allocated_memory_gb": allocated_memory_gb
            }
        else:
            return {"error": f"No data found for {team_name} in the collection."}

    except Exception as e:
        return {"error": f"Failed to fetch data from MongoDB: {str(e)}"}

def update_resources(db_name, team_name, mongodb_uri, allocated_cpu, allocated_memory_gb):
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongodb_uri)
        db = client[db_name]
        collection = db[team_name]

        # Update the allocated resources
        result = collection.update_one(
            {},
            {"$set": {"Allocated_CPU": allocated_cpu, "Allocated_Memory": allocated_memory_gb}}
        )

        if result.matched_count == 0:
            return {"error": f"No document found for {team_name} to update."}
        else:
            return {"success": f"Updated resources for {team_name}: CPU={allocated_cpu}, Memory={allocated_memory_gb} GB"}

    except Exception as e:
        return {"error": f"Failed to update MongoDB: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({"error": "Usage: python3 fetch_resources.py <db_name> <team_name> <mongodb_uri> [update <allocated_cpu> <allocated_memory_gb>]"}))
        sys.exit(1)

    db_name = sys.argv[1]
    team_name = sys.argv[2]
    mongodb_uri = sys.argv[3]

    if len(sys.argv) == 6 and sys.argv[4] == "update":
        allocated_cpu = int(sys.argv[5])
        allocated_memory_gb = int(sys.argv[6])
        result = update_resources(db_name, team_name, mongodb_uri, allocated_cpu, allocated_memory_gb)
    else:
        result = fetch_resources(db_name, team_name, mongodb_uri)

    print(json.dumps(result))
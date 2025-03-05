import pymongo
import sys
import json

def fetch_resources(db_name, team_name, mongodb_uri):
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongodb_uri)
        db = client[db_name]  # Database is now dynamic
        
        # Use the team name as the collection name (dynamic)
        collection = db[team_name]

        # Fetch allocated resources for the team
        team_data = collection.find_one({})  # Fetch first document in the collection

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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Usage: python3 fetch_resources.py <db_name> <team_name> <mongodb_uri>"}))
        sys.exit(1)

    db_name = sys.argv[1]
    team_name = sys.argv[2]
    mongodb_uri = sys.argv[3]

    result = fetch_resources(db_name, team_name, mongodb_uri)

    print(json.dumps(result))
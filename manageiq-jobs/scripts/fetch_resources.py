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
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_resources(db_name, team_name, mongodb_uri, action=None, cpu=None, memory=None):
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
                return {"error": "Required fields (Allocated_CPU or Allocated_Memory) missing in MongoDB document"}

            # Ensure values are numeric
            allocated_cpu = int(allocated_cpu)
            allocated_memory_gb = int(allocated_memory_gb)

            # If action is "create", subtract resources
            if action == "create" and cpu and memory:
                logging.info(f"Subtracting CPU {cpu} and Memory {memory}GB")
                new_cpu = allocated_cpu - int(cpu)
                new_memory = allocated_memory_gb - int(memory)
                result = collection.update_one({}, {"$set": {"Allocated_CPU": new_cpu, "Allocated_Memory": new_memory}})
                logging.info(f"Update result: {result.raw_result}")
                return {"message": f"Subtracted CPU {cpu} and Memory {memory}GB. New values: CPU={new_cpu}, Memory={new_memory}GB"}

            # If action is "delete", add back resources
            if action == "delete" and cpu and memory:
                logging.info(f"Adding back CPU {cpu} and Memory {memory}GB")
                new_cpu = allocated_cpu + int(cpu)
                new_memory = allocated_memory_gb + int(memory)
                result = collection.update_one({}, {"$set": {"Allocated_CPU": new_cpu, "Allocated_Memory": new_memory}})
                logging.info(f"Update result: {result.raw_result}")
                return {"message": f"Added back CPU {cpu} and Memory {memory}GB. New values: CPU={new_cpu}, Memory={new_memory}GB"}

            # If no action, return current allocated resources
            return {
                "allocated_cpu": allocated_cpu,
                "allocated_memory_gb": allocated_memory_gb
            }
        else:
            return {"error": f"No data found for {team_name} in the collection."}

    except Exception as e:
        logging.error(f"Failed to fetch data from MongoDB: {str(e)}")
        return {"error": f"Failed to fetch data from MongoDB: {str(e)}"}
    finally:
        # Close the MongoDB connection
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({"error": "Usage: python3 fetch_resources.py <db_name> <team_name> <mongodb_uri> [create|delete <cpu> <memory>]"}))
        sys.exit(1)

    db_name = sys.argv[1]
    team_name = sys.argv[2]
    mongodb_uri = sys.argv[3]

    # Optional create/delete parameters
    action = sys.argv[4] if len(sys.argv) > 4 else None
    cpu = sys.argv[5] if len(sys.argv) > 5 else None
    memory = sys.argv[6] if len(sys.argv) > 6 else None

    result = fetch_resources(db_name, team_name, mongodb_uri, action, cpu, memory)

    print(json.dumps(result))
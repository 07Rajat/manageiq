# import pymongo
# import json
# import logging
# from datetime import datetime
# from openai import OpenAI
# from bson import ObjectId
# import time  # For rate limiting

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # MongoDB connection details
# MONGODB_URI = "mongodb+srv://rajatnirmalkar35:fmDeFQNulNNEwBwq@manageiq.sm7ns.mongodb.net/?retryWrites=true&w=majority&appName=manageiq"
# DB_NAME = "Squads"
# COLLECTION_NAME = "Squad_Dev"

# # OpenAI API key
# OPENAI_API_KEY = "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"  # Replace with your OpenAI API key

# # Rate limiting (e.g., 1 request per second)
# RATE_LIMIT_DELAY = 1  # Delay in seconds between API calls

# def fetch_mongodb_data():
#     """
#     Fetch data from MongoDB.
#     """
#     try:
#         # Connect to MongoDB with a timeout
#         client = pymongo.MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
#         db = client[DB_NAME]
#         collection = db[COLLECTION_NAME]

#         # Fetch pipeline execution data
#         pipeline_data = list(collection.find({}))
#         return pipeline_data
#     except pymongo.errors.ServerSelectionTimeoutError as e:
#         logging.error(f"Failed to fetch MongoDB data: DNS resolution or connection timeout. Error: {str(e)}")
#         return []
#     except pymongo.errors.OperationFailure as e:
#         logging.error(f"Failed to fetch MongoDB data: Authentication failed. Error: {str(e)}")
#         return []
#     except Exception as e:
#         logging.error(f"Failed to fetch MongoDB data: {str(e)}")
#         return []
#     finally:
#         if 'client' in locals():
#             client.close()

# def convert_objectid_to_str(data):
#     """
#     Recursively convert ObjectId fields to strings in MongoDB data.
#     """
#     if isinstance(data, list):
#         return [convert_objectid_to_str(item) for item in data]
#     elif isinstance(data, dict):
#         return {key: convert_objectid_to_str(value) for key, value in data.items()}
#     elif isinstance(data, ObjectId):
#         return str(data)  # Convert ObjectId to string
#     else:
#         return data

# def generate_insights(mongodb_data):
#     """
#     Generate insights using OpenAI's GPT-4 model based on MongoDB data.
#     """
#     try:
#         # Convert ObjectId fields to strings
#         mongodb_data = convert_objectid_to_str(mongodb_data)

#         # Convert MongoDB data to JSON for AI analysis
#         data_str = json.dumps(mongodb_data, indent=2)

#         # Use ChatGPT to generate insights
#         client = OpenAI(api_key=OPENAI_API_KEY)
#         response = client.chat.completions.create(
#             model="gpt-4",  # Use GPT-4 or GPT-3.5-turbo
#             messages=[
#                 {"role": "system", "content": "You are a DevOps engineer analyzing MongoDB data."},
#                 {"role": "user", "content": f"Analyze the following MongoDB data and generate a report:\n{data_str}"}
#             ]
#         )

#         # Extract insights from the AI response
#         insights = response.choices[0].message.content
#         return insights
#     except Exception as e:
#         logging.error(f"Failed to generate insights: {str(e)}")
#         return "Error generating insights."

# def save_report(insights):
#     """
#     Save the generated insights to a file.
#     """
#     try:
#         # Save the report to a file
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         report_filename = f"mongodb_report_{timestamp}.txt"
#         with open(report_filename, "w") as f:
#             f.write(insights)
#         logging.info(f"Report saved to {report_filename}")
#     except Exception as e:
#         logging.error(f"Failed to save report: {str(e)}")

# if __name__ == "__main__":
#     # Fetch MongoDB data
#     mongodb_data = fetch_mongodb_data()

#     if mongodb_data:  # Proceed only if MongoDB data is fetched successfully
#         # Generate insights using AI
#         try:
#             insights = generate_insights(mongodb_data)
#             # Save the report
#             save_report(insights)
#         except Exception as e:
#             logging.error(f"Error during insights generation: {str(e)}")
#         finally:
#             # Add rate limiting delay
#             time.sleep(RATE_LIMIT_DELAY)
#     else:
#         logging.error("No MongoDB data fetched. Skipping insights generation.")

import pymongo
import json
import logging
from datetime import datetime
from openai import OpenAI
from bson import ObjectId
import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_mongodb_data(mongodb_uri, database, collection):
    """
    Fetch data from MongoDB.
    """
    try:
        client = pymongo.MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        db = client[database]
        collection = db[collection]
        pipeline_data = list(collection.find({}, {"Allocated_CPU": 1, "Allocated_Memory": 1, "_id": 1, "updates": 1}))
        return pipeline_data
    except Exception as e:
        logging.error(f"Failed to fetch MongoDB data from {collection}: {str(e)}")
        return []
    finally:
        if 'client' in locals():
            client.close()

def extract_latest_values(document):
    """
    Extract the latest values for Allocated_CPU and Allocated_Memory.
    If updates array is present, use the latest entry. Otherwise, use the top-level fields.
    """
    if "updates" in document and len(document["updates"]) > 0:
        # Use the latest entry in the updates array
        latest_update = document["updates"][-1]
        return {
            "_id": document["_id"],
            "Allocated_CPU": latest_update.get("Allocated_CPU", document.get("Allocated_CPU", 0)),
            "Allocated_Memory": latest_update.get("Allocated_Memory", document.get("Allocated_Memory", 0))
        }
    else:
        # Use the top-level fields
        return {
            "_id": document["_id"],
            "Allocated_CPU": document.get("Allocated_CPU", 0),
            "Allocated_Memory": document.get("Allocated_Memory", 0)
        }

def convert_objectid_to_str(data):
    """
    Recursively convert ObjectId fields to strings in MongoDB data.
    """
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

def generate_insights(mongodb_data, collection, openai_api_key):
    """
    Generate insights using OpenAI's GPT-4 model.
    """
    try:
        mongodb_data = convert_objectid_to_str(mongodb_data)
        data_str = json.dumps(mongodb_data, indent=2)

        client = OpenAI(api_key=openai_api_key)

        # Generate insights for resource allocation
        response_allocation = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a DevOps engineer analyzing MongoDB data related to resource allocation."},
                {"role": "user", "content": f"Analyze the following MongoDB data and generate a detailed report. Focus on CPU and memory allocations, and provide recommendations if the allocations seem unusual:\n{data_str}"}
            ]
        )
        insights_allocation = response_allocation.choices[0].message.content

        # Generate insights for trend analysis
        response_trends = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a DevOps engineer analyzing MongoDB data related to resource allocation over time."},
                {"role": "user", "content": f"Analyze the following MongoDB data and identify trends or anomalies in CPU and memory allocations:\n{data_str}"}
            ]
        )
        insights_trends = response_trends.choices[0].message.content

        # Generate insights for optimization suggestions
        response_optimization = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a DevOps engineer analyzing MongoDB data related to resource allocation."},
                {"role": "user", "content": f"Analyze the following MongoDB data and suggest optimizations for CPU and memory usage:\n{data_str}"}
            ]
        )
        insights_optimization = response_optimization.choices[0].message.content

        # Combine all insights into one report
        combined_insights = f"Resource Allocation Report:\n{insights_allocation}\n\nTrend Analysis Report:\n{insights_trends}\n\nOptimization Suggestions:\n{insights_optimization}"
        return combined_insights
    except Exception as e:
        logging.error(f"Failed to generate insights: {str(e)}")
        return "Error generating insights."

def create_visualizations(data, collection, report_dir):
    """
    Create bar graphs and spreadsheets for the data.
    """
    try:
        # Create a DataFrame
        df = pd.DataFrame(data)

        # Check if required fields exist
        if "Allocated_CPU" not in df.columns or "Allocated_Memory" not in df.columns:
            logging.warning(f"Required fields (Allocated_CPU, Allocated_Memory) not found in data for {collection}. Skipping visualizations.")
            return

        # Bar graph for Allocated_CPU and Allocated_Memory
        plt.figure(figsize=(10, 5))
        df.plot(kind="bar", x="_id", y=["Allocated_CPU", "Allocated_Memory"], title=f"Resource Allocation in {collection}")
        plt.savefig(os.path.join(report_dir, f"{collection}_bar_graph.png"))
        plt.close()

        # Save data to a spreadsheet
        spreadsheet_filename = os.path.join(report_dir, f"{collection}_data.xlsx")
        df.to_excel(spreadsheet_filename, index=False)
        logging.info(f"Spreadsheet saved to {spreadsheet_filename}")
    except Exception as e:
        logging.error(f"Failed to create visualizations: {str(e)}")

def save_report(insights, collection, report_dir):
    """
    Save the generated insights and visualizations to files.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = os.path.join(report_dir, f"{collection}_report_{timestamp}.txt")
        with open(report_filename, "w") as f:
            f.write(insights)
        logging.info(f"Report saved to {report_filename}")
        return report_filename
    except Exception as e:
        logging.error(f"Failed to save report: {str(e)}")
        return None

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate MongoDB resource allocation reports.")
    parser.add_argument("--mongodb_uri", required=True, help="MongoDB connection URI")
    parser.add_argument("--database", required=True, help="MongoDB database name")
    parser.add_argument("--collections", required=True, help="Comma-separated list of collections")
    parser.add_argument("--openai_api_key", required=True, help="OpenAI API key")
    parser.add_argument("--report_dir", default="reports", help="Directory to save reports (default: 'reports')")
    parser.add_argument("--rate_limit_delay", type=int, default=1, help="Rate limit delay in seconds (default: 1)")
    args = parser.parse_args()

    # Ensure the report directory exists
    os.makedirs(args.report_dir, exist_ok=True)

    report_files = []
    for collection in args.collections.split(","):
        mongodb_data = fetch_mongodb_data(args.mongodb_uri, args.database, collection)
        if mongodb_data:
            # Extract the latest values for Allocated_CPU and Allocated_Memory
            processed_data = [extract_latest_values(doc) for doc in mongodb_data]
            insights = generate_insights(processed_data, collection, args.openai_api_key)
            create_visualizations(processed_data, collection, args.report_dir)
            report_filename = save_report(insights, collection, args.report_dir)
            if report_filename:
                report_files.extend([
                    report_filename,
                    os.path.join(args.report_dir, f"{collection}_bar_graph.png"),
                    os.path.join(args.report_dir, f"{collection}_data.xlsx")
                ])
            logging.info(f"Report and visualizations generated for {collection}.")
        else:
            logging.error(f"No data fetched for {collection}. Skipping insights generation.")
        time.sleep(args.rate_limit_delay)

    # Save the list of generated files to a temporary file for the email script
    with open(os.path.join(args.report_dir, "generated_files.txt"), "w") as f:
        f.write("\n".join(report_files))
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
        latest_update = document["updates"][-1]
        return {
            "_id": document["_id"],
            "Allocated_CPU": latest_update.get("Allocated_CPU", document.get("Allocated_CPU", 0)),
            "Allocated_Memory": latest_update.get("Allocated_Memory", document.get("Allocated_Memory", 0))
        }
    else:
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
    Generate insights using OpenAI's GPT-4o model.
    """
    try:
        mongodb_data = convert_objectid_to_str(mongodb_data)
        data_str = json.dumps(mongodb_data, indent=2)

        client = OpenAI(api_key=openai_api_key)

        response_allocation = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a DevOps engineer analyzing MongoDB data related to resource allocation."},
                {"role": "user", "content": f"Analyze the following MongoDB data and generate a detailed report. Focus on CPU and memory allocations, and provide recommendations if the allocations seem unusual:\n{data_str}"}
            ]
        )
        insights_allocation = response_allocation.choices[0].message.content

        response_trends = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a DevOps engineer analyzing MongoDB data related to resource allocation over time."},
                {"role": "user", "content": f"Analyze the following MongoDB data and identify trends or anomalies in CPU and memory allocations:\n{data_str}"}
            ]
        )
        insights_trends = response_trends.choices[0].message.content

        response_optimization = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a DevOps engineer analyzing MongoDB data related to resource allocation."},
                {"role": "user", "content": f"Analyze the following MongoDB data and suggest optimizations for CPU and memory usage:\n{data_str}"}
            ]
        )
        insights_optimization = response_optimization.choices[0].message.content

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

        df = pd.DataFrame(data)

        if "Allocated_CPU" not in df.columns or "Allocated_Memory" not in df.columns:
            logging.warning(f"Required fields (Allocated_CPU, Allocated_Memory) not found in data for {collection}. Skipping visualizations.")
            return

        plt.figure(figsize=(10, 5))
        df.plot(kind="bar", x="_id", y=["Allocated_CPU", "Allocated_Memory"], title=f"Resource Allocation in {collection}")
        plt.savefig(os.path.join(report_dir, f"{collection}_bar_graph.png"))
        plt.close()

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

    parser = argparse.ArgumentParser(description="Generate MongoDB resource allocation reports.")
    parser.add_argument("--mongodb_uri", required=True, help="MongoDB connection URI")
    parser.add_argument("--database", required=True, help="MongoDB database name")
    parser.add_argument("--collections", required=True, help="Comma-separated list of collections")
    parser.add_argument("--openai_api_key", required=True, help="OpenAI API key")
    parser.add_argument("--report_dir", default="reports", help="Directory to save reports (default: 'reports')")
    parser.add_argument("--rate_limit_delay", type=int, default=1, help="Rate limit delay in seconds (default: 1)")
    args = parser.parse_args()

    os.makedirs(args.report_dir, exist_ok=True)

    report_files = []
    for collection in args.collections.split(","):
        mongodb_data = fetch_mongodb_data(args.mongodb_uri, args.database, collection)
        if mongodb_data:
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

    with open(os.path.join(args.report_dir, "generated_files.txt"), "w") as f:
        f.write("\n".join(report_files))
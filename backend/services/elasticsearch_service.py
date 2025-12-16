from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

# Elasticsearch connection
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

try:
    es = Elasticsearch([ELASTICSEARCH_URL])
    # Test connection
    if not es.ping():
        print("Warning: Elasticsearch connection failed, continuing without it")
        es = None
except Exception as e:
    print(f"Warning: Elasticsearch not available: {e}")
    es = None

def index_log(log_data):
    """Index a log entry in Elasticsearch"""
    if not es:
        return None
    
    try:
        return es.index(
            index="securewatch-logs",
            body={
                "timestamp": log_data.get("timestamp"),
                "source_ip": log_data.get("source_ip"),
                "destination_ip": log_data.get("destination_ip"),
                "log_type": log_data.get("log_type"),
                "raw_log": log_data.get("raw_log"),
                "message": log_data.get("message"),
                "severity": log_data.get("severity", "low")
            }
        )
    except Exception as e:
        print(f"Elasticsearch indexing error: {e}")
        return None

def search_logs(query, size=100):
    """Search logs in Elasticsearch"""
    if not es:
        return {"hits": {"hits": []}}
    
    try:
        return es.search(
            index="securewatch-logs",
            body={"query": query},
            size=size
        )
    except Exception as e:
        print(f"Elasticsearch search error: {e}")
        return {"hits": {"hits": []}}


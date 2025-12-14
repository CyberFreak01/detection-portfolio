#!/usr/bin/env python3
"""
Verify that detections fired in Elastic after Atomic tests
"""
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from elasticsearch import Elasticsearch
from utils import (setup_logging, load_yaml, get_technique_from_filename,
                   print_success, print_error, print_info)

logger = setup_logging(__name__)

def verify_detection(technique: str, test_num: str, es_client, config: dict) -> bool:
    """Verify detection alert exists in Elastic"""
    try:
        # Query for alerts from last 10 minutes
        time_range = datetime.utcnow() - timedelta(minutes=10)
        
        query = {
            "bool": {
                "must": [
                    {"match": {"tags": f"technique:{technique}"}},
                    {"range": {"@timestamp": {"gte": time_range.isoformat()}}}
                ]
            }
        }
        
        print_info(f"Searching for alerts matching {technique}...")
        
        response = es_client.search(
            index=".alerts-security.alerts-default",
            body={"query": query, "size": 10},
            timeout="30s"
        )
        
        hits = response["hits"]["total"]["value"]
        
        if hits > 0:
            print_success(f"✓ Detection verified: {hits} alert(s) found for {technique} #{test_num}")
            return True
        else:
            print_error(f"✗ No alerts found for {technique} #{test_num}")
            return False
            
    except Exception as e:
        print_error(f"Error verifying detection: {str(e)}")
        return False

def main():
    rules_dir = Path("rules/sigma")
    config_file = Path("config/elastic_config.yml")
    
    if not config_file.exists():
        print_error(f"Elastic config not found: {config_file}")
        sys.exit(1)
    
    config = load_yaml(str(config_file))
    env = config["environments"]["test"]
    
    # Connect to Elasticsearch
    try:
        es_client = Elasticsearch(
            [env["url"]],
            api_key=env["api_key"],
            verify_certs=True,
            request_timeout=30
        )
        
        if not es_client.ping():
            print_error("Could not connect to Elasticsearch")
            sys.exit(1)
            
        print_success("Connected to Elasticsearch")
        
    except Exception as e:
        print_error(f"Elasticsearch connection error: {str(e)}")
        sys.exit(1)
    
    rule_files = list(rules_dir.glob("*.yml"))
    
    print_info(f"Verifying detections for {len(rule_files)} rules...")
    print_info("Waiting additional 30 seconds for alert generation...")
    time.sleep(30)
    
    failed = 0
    for rule_file in rule_files:
        technique, test_num = get_technique_from_filename(rule_file.name)
        if technique and test_num:
            if not verify_detection(technique, test_num, es_client, config):
                failed += 1
    
    if failed > 0:
        print_error(f"{failed} detections not verified")
        sys.exit(1)
    else:
        print_success("All detections verified successfully")
        sys.exit(0)

if __name__ == "__main__":
    main()
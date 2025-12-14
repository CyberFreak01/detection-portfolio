#!/usr/bin/env python3
"""
Deploy detection rules to Elastic Security
"""
import sys
import os
from pathlib import Path
import requests
from utils import (setup_logging, load_yaml, load_json,
                   print_success, print_error, print_info)

logger = setup_logging(__name__)

def deploy_rule_to_elastic(rule_data: dict, elastic_url: str, api_key: str) -> bool:
    """Deploy single rule to Elastic"""
    try:
        headers = {
            "kbn-xsrf": "true",
            "Content-Type": "application/json",
            "Authorization": f"ApiKey {api_key}"
        }
        
        endpoint = f"{elastic_url}/api/detection_engine/rules"
        
        # Check if rule already exists
        rule_id = rule_data.get("rule_id", rule_data["name"].lower().replace(" ", "_"))
        rule_data["rule_id"] = rule_id
        
        # Try to get existing rule
        get_response = requests.get(
            f"{endpoint}?rule_id={rule_id}",
            headers=headers,
            timeout=30
        )
        
        if get_response.status_code == 200:
            # Update existing rule
            existing_rule = get_response.json()
            rule_data["id"] = existing_rule["id"]
            
            response = requests.put(
                endpoint,
                json=rule_data,
                headers=headers,
                timeout=30
            )
            action = "Updated"
        else:
            # Create new rule
            response = requests.post(
                endpoint,
                json=rule_data,
                headers=headers,
                timeout=30
            )
            action = "Created"
        
        if response.status_code in [200, 201]:
            print_success(f"{action} rule: {rule_data['name']}")
            return True
        else:
            print_error(f"Failed to deploy rule: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request error: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error deploying rule: {str(e)}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy rules to Elastic")
    parser.add_argument("--env", choices=["test", "prod"], required=True,
                       help="Target environment")
    args = parser.parse_args()
    
    # Load configuration
    config_file = Path("config/elastic_config.yml")
    if not config_file.exists():
        print_error(f"Config file not found: {config_file}")
        sys.exit(1)
    
    config = load_yaml(str(config_file))
    env_config = config["environments"][args.env]
    
    # Get API key from environment variable or config
    api_key = os.environ.get(f"ELASTIC_{args.env.upper()}_API_KEY") or env_config["api_key"]
    
    if not api_key or api_key.startswith("${"):
        print_error(f"API key not configured for {args.env} environment")
        sys.exit(1)
    
    elastic_url = env_config["url"]
    
    # Load converted rules
    rules_dir = Path("rules-converted/elastic")
    
    if not rules_dir.exists():
        print_error(f"Converted rules directory not found: {rules_dir}")
        sys.exit(1)
    
    rule_files = list(rules_dir.glob("*.json"))
    
    if not rule_files:
        print_error("No converted rules found")
        sys.exit(1)
    
    print_info(f"Deploying {len(rule_files)} rules to {args.env} environment...")
    
    failed = 0
    for rule_file in rule_files:
        rule_data = load_json(str(rule_file))
        if not deploy_rule_to_elastic(rule_data, elastic_url, api_key):
            failed += 1
    
    if failed > 0:
        print_error(f"{failed}/{len(rule_files)} rules failed to deploy")
        sys.exit(1)
    else:
        print_success(f"All {len(rule_files)} rules deployed successfully to {args.env}")
        sys.exit(0)

if __name__ == "__main__":
    main()
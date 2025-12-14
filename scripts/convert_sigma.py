#!/usr/bin/env python3
"""
Convert Sigma rules to Elastic EQL using sigma-cli
"""
import sys
import subprocess
import json
from pathlib import Path
from utils import (setup_logging, load_yaml, save_json, 
                   get_technique_from_filename, print_success, 
                   print_error, print_info)

logger = setup_logging(__name__)

def convert_sigma_to_eql(sigma_file: str, output_file: str) -> bool:
    """Convert single Sigma rule to Elastic EQL"""
    try:
        # Use sigma-cli with elasticsearch backend and sysmon pipeline
        result = subprocess.run(
            [
                "sigma", "convert",
                "-t", "elasticsearch",
                "-p", "ecs_windows",
                "-f", "eql",
                sigma_file
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print_error(f"Conversion failed for {sigma_file}")
            logger.error(result.stderr)
            return False
        
        eql_query = result.stdout.strip()
        
        # Load original Sigma rule for metadata
        sigma_rule = load_yaml(sigma_file)
        technique, test_num = get_technique_from_filename(sigma_file)
        
        # Create Elastic detection rule format
        elastic_rule = {
            "name": sigma_rule.get("title", "Unnamed Rule"),
            "description": sigma_rule.get("description", ""),
            "risk_score": get_risk_score(sigma_rule.get("level", "medium")),
            "severity": sigma_rule.get("level", "medium"),
            "type": "eql",
            "language": "eql",
            "query": eql_query,
            "tags": sigma_rule.get("tags", []) + [f"technique:{technique}"],
            "references": sigma_rule.get("references", []),
            "false_positives": sigma_rule.get("falsepositives", []),
            "author": [sigma_rule.get("author", "Unknown")],
            "enabled": True,
            "interval": "5m",
            "from": "now-6m",
            "index": ["logs-endpoint.events.*", "winlogbeat-*"],
            "max_signals": 100,
            "threat": get_mitre_threat(sigma_rule.get("tags", []))
        }
        
        # Save converted rule
        save_json(elastic_rule, output_file)
        print_success(f"Converted: {sigma_file} -> {output_file}")
        return True
        
    except subprocess.TimeoutExpired:
        print_error(f"Conversion timeout for {sigma_file}")
        return False
    except Exception as e:
        print_error(f"Error converting {sigma_file}: {str(e)}")
        return False

def get_risk_score(level: str) -> int:
    """Map Sigma severity to Elastic risk score"""
    mapping = {
        "informational": 21,
        "low": 47,
        "medium": 73,
        "high": 99,
        "critical": 99
    }
    return mapping.get(level.lower(), 47)

def get_mitre_threat(tags: list) -> list:
    """Extract MITRE ATT&CK info from tags"""
    threats = []
    
    for tag in tags:
        if tag.startswith("attack.t"):
            technique_id = tag.replace("attack.", "").upper()
            
            # Parse technique and sub-technique
            if "." in technique_id:
                tactic_technique = technique_id.split(".")
                technique = tactic_technique[0]
                subtechnique = technique_id
            else:
                technique = technique_id
                subtechnique = None
            
            threat_entry = {
                "framework": "MITRE ATT&CK",
                "technique": [{
                    "id": technique,
                    "name": f"Technique {technique}",
                    "reference": f"https://attack.mitre.org/techniques/{technique}/"
                }]
            }
            
            if subtechnique:
                threat_entry["technique"][0]["subtechnique"] = [{
                    "id": subtechnique,
                    "name": f"Sub-technique {subtechnique}",
                    "reference": f"https://attack.mitre.org/techniques/{subtechnique.replace('.', '/')}/"
                }]
            
            threats.append(threat_entry)
    
    return threats

def main():
    sigma_dir = Path("rules/sigma")
    output_dir = Path("rules-converted/elastic")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not sigma_dir.exists():
        print_error(f"Sigma rules directory not found: {sigma_dir}")
        sys.exit(1)
    
    sigma_files = list(sigma_dir.glob("*.yml"))
    
    if not sigma_files:
        print_error("No Sigma rules found")
        sys.exit(1)
    
    print_info(f"Converting {len(sigma_files)} Sigma rules to Elastic EQL...")
    
    failed = 0
    for sigma_file in sigma_files:
        output_file = output_dir / f"{sigma_file.stem}.json"
        if not convert_sigma_to_eql(str(sigma_file), str(output_file)):
            failed += 1
    
    if failed > 0:
        print_error(f"{failed}/{len(sigma_files)} conversions failed")
        sys.exit(1)
    else:
        print_success(f"All {len(sigma_files)} rules converted successfully")
        sys.exit(0)

if __name__ == "__main__":
    main()
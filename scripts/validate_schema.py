#!/usr/bin/env python3
"""
Validate Sigma rule schema and structure
"""
import sys
from pathlib import Path
from jsonschema import validate, ValidationError
from utils import setup_logging, load_yaml, print_success, print_error

logger = setup_logging(__name__)

SIGMA_SCHEMA = {
    "type": "object",
    "required": ["title", "logsource", "detection"],
    "properties": {
        "title": {"type": "string"},
        "id": {"type": "string"},
        "status": {"type": "string", "enum": ["stable", "test", "experimental"]},
        "description": {"type": "string"},
        "references": {"type": "array"},
        "author": {"type": "string"},
        "date": {"type": "string"},
        "modified": {"type": "string"},
        "tags": {"type": "array"},
        "logsource": {
            "type": "object",
            "required": ["category", "product"],
            "properties": {
                "category": {"type": "string"},
                "product": {"type": "string"}
            }
        },
        "detection": {"type": "object"},
        "falsepositives": {"type": "array"},
        "level": {"type": "string", "enum": ["informational", "low", "medium", "high", "critical"]}
    }
}

def validate_sigma_schema(rule_file: str) -> bool:
    """Validate Sigma rule against schema"""
    try:
        rule = load_yaml(rule_file)
        validate(instance=rule, schema=SIGMA_SCHEMA)
        
        # Additional checks
        if 'tags' in rule:
            mitre_tags = [tag for tag in rule['tags'] if tag.startswith('attack.t')]
            if not mitre_tags:
                print_warning(f"{rule_file}: No MITRE ATT&CK tags found")
        
        print_success(f"Schema validation passed: {rule_file}")
        return True
        
    except ValidationError as e:
        print_error(f"Schema validation failed for {rule_file}: {e.message}")
        return False
    except Exception as e:
        print_error(f"Error validating {rule_file}: {str(e)}")
        return False

def main():
    rules_dir = Path("rules/sigma")
    
    if not rules_dir.exists():
        print_error(f"Rules directory not found: {rules_dir}")
        sys.exit(1)
    
    rule_files = list(rules_dir.glob("*.yml"))
    
    if not rule_files:
        print_error("No Sigma rules found")
        sys.exit(1)
    
    print_info(f"Validating {len(rule_files)} Sigma rules...")
    
    failed = 0
    for rule_file in rule_files:
        if not validate_sigma_schema(str(rule_file)):
            failed += 1
    
    if failed > 0:
        print_error(f"{failed}/{len(rule_files)} rules failed schema validation")
        sys.exit(1)
    else:
        print_success(f"All {len(rule_files)} rules passed schema validation")
        sys.exit(0)

if __name__ == "__main__":
    main()
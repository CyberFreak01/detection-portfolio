#!/usr/bin/env python3
"""
Validate that test data contains required fields for detection
"""
import sys
from pathlib import Path
from utils import (setup_logging, load_json, get_technique_from_filename,
                   print_success, print_error, print_info, print_warning)

logger = setup_logging(__name__)

def validate_test_data_fields(technique: str, test_num: str) -> bool:
    """Validate test data has required fields"""
    test_data_dir = Path("test-data")
    
    # Load required fields mapping
    fields_file = test_data_dir / f"{technique.lower()}_{test_num}_fields.json"
    sample_file = test_data_dir / f"{technique.lower()}_{test_num}_sample.json"
    
    if not fields_file.exists():
        print_warning(f"No field mapping found for {technique}_{test_num}")
        return True  # Not critical, continue
    
    try:
        required_fields = load_json(str(fields_file))
        
        if sample_file.exists():
            sample_data = load_json(str(sample_file))
            
            # Check if sample contains required fields
            missing_fields = []
            for field in required_fields.get("required_fields", []):
                if not check_nested_field(sample_data, field):
                    missing_fields.append(field)
            
            if missing_fields:
                print_error(f"Sample data missing fields: {', '.join(missing_fields)}")
                return False
            
            print_success(f"Test data validation passed for {technique}_{test_num}")
        else:
            print_info(f"No sample data found for {technique}_{test_num}")
        
        return True
        
    except Exception as e:
        print_error(f"Error validating test data: {str(e)}")
        return False

def check_nested_field(data: dict, field_path: str) -> bool:
    """Check if nested field exists in data"""
    keys = field_path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False
    
    return True

def main():
    rules_dir = Path("rules/sigma")
    
    if not rules_dir.exists():
        print_error(f"Rules directory not found: {rules_dir}")
        sys.exit(1)
    
    rule_files = list(rules_dir.glob("*.yml"))
    
    print_info(f"Validating test data for {len(rule_files)} rules...")
    
    failed = 0
    for rule_file in rule_files:
        technique, test_num = get_technique_from_filename(rule_file.name)
        if technique and test_num:
            if not validate_test_data_fields(technique, test_num):
                failed += 1
    
    if failed > 0:
        print_error(f"{failed} test data validations failed")
        sys.exit(1)
    else:
        print_success("All test data validations passed")
        sys.exit(0)

if __name__ == "__main__":
    main()
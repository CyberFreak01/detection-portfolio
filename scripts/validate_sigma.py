#!/usr/bin/env python3
"""
Validate Sigma rules using sigma-cli
"""
import sys
import subprocess
from pathlib import Path
from utils import setup_logging, print_success, print_error, print_info

logger = setup_logging(__name__)

def validate_with_sigma_cli(rules_dir: str) -> bool:
    """Validate Sigma rules using sigma check command"""
    try:
        print_info("Running sigma-cli validation...")
        
        result = subprocess.run(
            ["sigma", "check", rules_dir],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print_success("Sigma-cli validation passed")
            logger.info(result.stdout)
            return True
        else:
            print_error("Sigma-cli validation failed")
            logger.error(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Sigma-cli validation timed out")
        return False
    except FileNotFoundError:
        print_error("sigma-cli not found. Install with: pip install sigma-cli")
        return False
    except Exception as e:
        print_error(f"Error running sigma-cli: {str(e)}")
        return False

def main():
    rules_dir = Path("rules/sigma")
    
    if not rules_dir.exists():
        print_error(f"Rules directory not found: {rules_dir}")
        sys.exit(1)
    
    if validate_with_sigma_cli(str(rules_dir)):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
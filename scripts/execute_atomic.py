#!/usr/bin/env python3
"""
Execute Atomic Red Team tests based on rule naming convention
"""
import sys
import subprocess
import time
from pathlib import Path
from utils import (setup_logging, load_yaml, get_technique_from_filename,
                   print_success, print_error, print_info)

logger = setup_logging(__name__)

def execute_atomic_test(technique: str, test_num: str, config: dict) -> bool:
    """Execute specific Atomic Red Team test"""
    try:
        atomic_path = Path(config.get("atomic_path", "./AtomicRedTeam"))
        executor = config.get("executor", "powershell")
        timeout = config.get("timeout", 300)
        
        print_info(f"Executing Atomic test {technique} #{test_num}...")
        
        if executor == "powershell":
            # PowerShell execution
            ps_command = f"""
            Import-Module {atomic_path}/invoke-atomicredteam/Invoke-AtomicRedTeam.psd1
            Invoke-AtomicTest {technique} -TestNumbers {test_num} -ExecutionLogPath ./execution.log
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=timeout
            )
        else:
            # Bash execution for Linux
            result = subprocess.run(
                [
                    "bash",
                    f"{atomic_path}/atomics/{technique}/{test_num}.sh"
                ],
                capture_output=True,
                text=True,
                timeout=timeout
            )
        
        if result.returncode == 0:
            print_success(f"Atomic test {technique} #{test_num} executed successfully")
            logger.info(result.stdout)
            
            # Wait for logs to be ingested
            print_info("Waiting 60 seconds for log ingestion...")
            time.sleep(60)
            return True
        else:
            print_error(f"Atomic test {technique} #{test_num} failed")
            logger.error(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error(f"Atomic test {technique} #{test_num} timed out")
        return False
    except Exception as e:
        print_error(f"Error executing Atomic test: {str(e)}")
        return False

def cleanup_atomic_test(technique: str, test_num: str, config: dict):
    """Cleanup after Atomic test"""
    try:
        if not config.get("cleanup", True):
            return
        
        atomic_path = Path(config.get("atomic_path", "./AtomicRedTeam"))
        executor = config.get("executor", "powershell")
        
        print_info(f"Cleaning up Atomic test {technique} #{test_num}...")
        
        if executor == "powershell":
            ps_command = f"""
            Import-Module {atomic_path}/invoke-atomicredteam/Invoke-AtomicRedTeam.psd1
            Invoke-AtomicTest {technique} -TestNumbers {test_num} -Cleanup
            """
            
            subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                timeout=60
            )
        
        print_success(f"Cleanup completed for {technique} #{test_num}")
        
    except Exception as e:
        print_error(f"Error during cleanup: {str(e)}")

def main():
    rules_dir = Path("rules/sigma")
    config_file = Path("config/atomic_config.yml")
    
    if not rules_dir.exists():
        print_error(f"Rules directory not found: {rules_dir}")
        sys.exit(1)
    
    config = load_yaml(str(config_file)) if config_file.exists() else {}
    
    rule_files = list(rules_dir.glob("*.yml"))
    
    print_info(f"Executing Atomic tests for {len(rule_files)} rules...")
    
    failed = 0
    for rule_file in rule_files:
        technique, test_num = get_technique_from_filename(rule_file.name)
        if technique and test_num:
            if execute_atomic_test(technique, test_num, config):
                cleanup_atomic_test(technique, test_num, config)
            else:
                failed += 1
        else:
            print_warning(f"Could not parse technique from {rule_file.name}")
    
    if failed > 0:
        print_error(f"{failed} Atomic tests failed")
        sys.exit(1)
    else:
        print_success("All Atomic tests executed successfully")
        sys.exit(0)

if __name__ == "__main__":
    main()
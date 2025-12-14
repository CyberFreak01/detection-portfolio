import yaml
import json
import logging
from pathlib import Path
from typing import Dict, Any
from colorama import Fore, Style, init

init(autoreset=True)

def setup_logging(name: str) -> logging.Logger:
    """Setup colored logging"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        f'{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - '
        f'{Fore.GREEN}%(name)s{Style.RESET_ALL} - '
        f'%(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def load_yaml(file_path: str) -> Dict[Any, Any]:
    """Load YAML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_json(file_path: str) -> Dict[Any, Any]:
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Dict[Any, Any], file_path: str):
    """Save JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_technique_from_filename(filename: str) -> tuple:
    """
    Extract technique and test number from filename
    Example: t1003.001_1.yml -> ('t1003.001', '1')
    """
    stem = Path(filename).stem
    parts = stem.split('_')
    if len(parts) == 2:
        technique = parts[0].upper()
        test_num = parts[1]
        return technique, test_num
    return None, None

def print_success(message: str):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message: str):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_warning(message: str):
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def print_info(message: str):
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")
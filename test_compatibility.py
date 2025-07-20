#!/usr/bin/env python3
"""
Compatibility test for the CrowdStrike Correlation Rules Backup Tool
"""
import sys
import importlib
from typing import List, Tuple

def test_python_version() -> Tuple[bool, str]:
    """Test if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        return True, f"Python {version.major}.{version.minor}.{version.micro} - Compatible"
    else:
        return False, f"Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+"

def test_required_packages() -> List[Tuple[str, bool, str]]:
    """Test if required packages are available"""
    required_packages = [
        "falconpy",
        "click", 
        "rich",
        "dotenv",
        "requests"
    ]
    
    results = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            results.append((package, True, "Available"))
        except ImportError:
            results.append((package, False, "Missing"))
    
    return results

def test_config_import() -> Tuple[bool, str]:
    """Test if config module can be imported"""
    try:
        from config import Config
        return True, "Config module imported successfully"
    except ImportError as e:
        return False, f"Config import failed: {str(e)}"

def test_utils_import() -> Tuple[bool, str]:
    """Test if utils modules can be imported"""
    try:
        from utils.logger import setup_logger
        from utils.validators import sanitize_filename
        return True, "Utils modules imported successfully"
    except ImportError as e:
        return False, f"Utils import failed: {str(e)}"

def test_tools_import() -> Tuple[bool, str]:
    """Test if tools modules can be imported"""
    try:
        from tools.correlation_rules_backup import backup_all_correlation_rules
        return True, "Tools modules imported successfully"
    except ImportError as e:
        return False, f"Tools import failed: {str(e)}"

def main():
    """Run all compatibility tests"""
    print("CrowdStrike Correlation Rules Backup Tool - Compatibility Test")
    print("=" * 60)
    
    # Test Python version
    py_compatible, py_message = test_python_version()
    print(f"Python Version: {py_message}")
    
    # Test required packages
    print("\nRequired Packages:")
    package_results = test_required_packages()
    for package, available, message in package_results:
        status = "PASS" if available else "FAIL"
        print(f"  {status} {package}: {message}")
    
    # Test local modules
    print("\nLocal Modules:")
    
    config_ok, config_msg = test_config_import()
    print(f"  {'PASS' if config_ok else 'FAIL'} config.py: {config_msg}")
    
    utils_ok, utils_msg = test_utils_import()
    print(f"  {'PASS' if utils_ok else 'FAIL'} utils/: {utils_msg}")
    
    tools_ok, tools_msg = test_tools_import()
    print(f"  {'PASS' if tools_ok else 'FAIL'} tools/: {tools_msg}")
    
    # Summary
    print("\n" + "=" * 60)
    all_packages_ok = all(result[1] for result in package_results)
    all_modules_ok = config_ok and utils_ok and tools_ok
    
    if py_compatible and all_packages_ok and all_modules_ok:
        print("SUCCESS: All compatibility tests passed!")
        print("The tool should work correctly on this system.")
        return 0
    else:
        print("ERROR: Some compatibility tests failed!")
        print("Please check the issues above before using the tool.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

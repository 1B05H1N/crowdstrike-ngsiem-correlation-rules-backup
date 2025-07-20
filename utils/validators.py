"""
Validation utilities for the CrowdStrike Correlation Rules Backup Tool
"""
import os
from typing import Dict, Any, Optional
from falconpy import CorrelationRules

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_api_credentials(client_id: str, client_secret: str) -> bool:
    """
    Validate API credentials by attempting to create a client
    
    Args:
        client_id: CrowdStrike API client ID
        client_secret: CrowdStrike API client secret
        
    Returns:
        True if credentials are valid
        
    Raises:
        ValidationError: If credentials are invalid
    """
    try:
        # Try to create a client to validate credentials
        client = CorrelationRules(
            client_id=client_id,
            client_secret=client_secret,
            cloud_region="us-2"  # Default region for validation
        )
        
        # Test the connection with a minimal API call
        response = client.get_rules_combined(limit=1)
        
        if response.get("status_code") == 200:
            return True
        else:
            raise ValidationError(f"API authentication failed: {response.get('status_code')}")
            
    except Exception as e:
        raise ValidationError(f"Invalid credentials: {str(e)}")

def validate_directory_path(path: str) -> bool:
    """
    Validate that a directory path is writable
    
    Args:
        path: Directory path to validate
        
    Returns:
        True if path is valid and writable
        
    Raises:
        ValidationError: If path is invalid or not writable
    """
    try:
        # Check if directory exists or can be created
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise ValidationError(f"Path exists but is not a directory: {path}")
        else:
            # Try to create the directory
            os.makedirs(path, exist_ok=True)
        
        # Check if directory is writable
        test_file = os.path.join(path, ".test_write")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except Exception as e:
            raise ValidationError(f"Directory is not writable: {path} - {str(e)}")
        
        return True
        
    except Exception as e:
        if isinstance(e, ValidationError):
            raise
        raise ValidationError(f"Invalid directory path: {path} - {str(e)}")

def validate_rule_data(rule: Dict[str, Any]) -> bool:
    """
    Validate that a rule object has required fields
    
    Args:
        rule: Rule data dictionary
        
    Returns:
        True if rule is valid
        
    Raises:
        ValidationError: If rule is missing required fields
    """
    required_fields = ["id"]
    optional_fields = ["name", "description", "status"]
    
    # Check required fields
    for field in required_fields:
        if field not in rule:
            raise ValidationError(f"Rule missing required field: {field}")
    
    # Check that optional fields are strings if present
    for field in optional_fields:
        if field in rule and not isinstance(rule[field], str):
            raise ValidationError(f"Rule field '{field}' must be a string")
    
    return True

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe file system usage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for file system
    """
    # Remove or replace problematic characters
    import re
    
    # Replace spaces with underscores
    sanitized = filename.replace(' ', '_')
    
    # Remove special characters except alphanumeric, underscore, hyphen, and dot
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', sanitized)
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed_file"
    
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized 
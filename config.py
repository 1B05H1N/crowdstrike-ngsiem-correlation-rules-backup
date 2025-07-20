"""
Configuration settings for the CrowdStrike Correlation Rules Backup Tool
"""
import os
from typing import Optional

class Config:
    """Configuration class for the backup tool"""
    
    # API Configuration
    FALCON_CLIENT_ID: Optional[str] = os.getenv("FALCON_CLIENT_ID")
    FALCON_CLIENT_SECRET: Optional[str] = os.getenv("FALCON_CLIENT_SECRET")
    FALCON_CLOUD_REGION: str = os.getenv("FALCON_CLOUDREGION", "us-2")
    
    # Backup Configuration
    BASE_EXPORT_DIR: str = "correlation_rules_backups"
    BACKUP_LIMIT: int = 500  # Number of rules per API call
    BACKUP_FILTER: str = os.getenv("BACKUP_FILTER", "*")  # Filter for correlation rules
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "[%(asctime)s] %(levelname)s: %(message)s"
    
    # File Configuration
    JSON_INDENT: int = 2
    ENCODING: str = "utf-8"
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """Validate that required credentials are set"""
        if not cls.FALCON_CLIENT_ID or not cls.FALCON_CLIENT_SECRET:
            return False
        return True
    
    @classmethod
    def get_credentials_error_message(cls) -> str:
        """Get error message for missing credentials"""
        return (
            "Error: FALCON_CLIENT_ID and FALCON_CLIENT_SECRET environment variables must be set.\n"
            "Please set these environment variables before running the script.\n"
            "Optional: Set FALCON_CLOUD_REGION (default: us-2)\n"
            "Optional: Set BACKUP_FILTER (default: *)"
        ) 
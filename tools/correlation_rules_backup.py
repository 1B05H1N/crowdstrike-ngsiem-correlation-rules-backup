import os
import json
from falconpy import CorrelationRules
from datetime import datetime
from utils.logger import setup_logger, get_log_filename
from config import Config

# You can change this to your desired folder path
BASE_EXPORT_DIR = "correlation_rules_backups" 

def save_json(path, data):
    """Save data to JSON file with proper error handling"""
    try:
        # Ensure the directory exists
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        # Save the JSON file
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        print(f"Successfully saved: {path}")
        return True
    except Exception as e:
        print(f"Error saving {path}: {str(e)}")
        return False

def backup_all_correlation_rules(client_id, client_secret, cloud_region, backup_filter=None):
    """
    Backup all correlation rules using falconpy
    
    Args:
        client_id (str): CrowdStrike API client ID
        client_secret (str): CrowdStrike API client secret
        cloud_region (str): CrowdStrike cloud region (default: us-2)
        backup_filter (str): Filter for correlation rules (default: from Config.BACKUP_FILTER)
    """
    # Setup logging
    log_file = get_log_filename()
    logger = setup_logger(log_file=log_file)
    
    logger.info("Starting correlation rules backup process")
    logger.info(f"Backup directory: {BASE_EXPORT_DIR}")
    
    try:
        # Create date based subfolder
        current_date = datetime.now().strftime("%Y-%m-%d")
        EXPORT_DIR = os.path.join(BASE_EXPORT_DIR, current_date)

        logger.info(f"Creating date based export directory: {EXPORT_DIR}")
        os.makedirs(EXPORT_DIR, exist_ok=True)
        logger.info(f"Export directory ready: {EXPORT_DIR}")
        
        # Initialize the CorrelationRules client
        logger.info("Initializing CrowdStrike API client")
        rules = CorrelationRules(
            client_id=client_id,
            client_secret=client_secret,
            cloud_region=cloud_region
        )

        # Get list of all rule IDs with pagination
        logger.info("Fetching all correlation rules...")
        all_responses = []
        all_rules = []
        offset = 0
        limit = Config.BACKUP_LIMIT
        filter = backup_filter if backup_filter is not None else Config.BACKUP_FILTER
        
        logger.info(f"Using filter: {filter}")
        
        while True:
            query_response = rules.get_rules_combined(limit=limit, offset=offset, filter=filter)
            
            if not query_response["status_code"] == 200:
                logger.error(f"Error fetching rules: {query_response['status_code']}")
                return
                
            # Save the complete API response with time (no date in filename since it's in folder)
            current_time = datetime.now().strftime("%H%M%S")
            response_filename = os.path.join(EXPORT_DIR, f"api_response_offset_{offset}_{current_time}.json")
            if save_json(response_filename, query_response):
                logger.info(f"API response saved: {response_filename}")
                # Verify file was actually created
                if os.path.exists(response_filename):
                    file_size = os.path.getsize(response_filename)
                    logger.info(f"  File size: {file_size} bytes")
                else:
                    logger.warning(f"  File not found after save attempt")
            else:
                logger.error(f"Failed to save API response: {response_filename}")
                
            current_rules = query_response["body"].get("resources", [])
            
            if not current_rules:
                break
                
            all_responses.append(query_response)
            all_rules.extend(current_rules)
            logger.info(f"Fetched {len(current_rules)} rules (offset: {offset})")
            
            # If we got fewer rules than the limit, we've reached the end
            if len(current_rules) < limit:
                break
                
            offset += limit

        if not all_responses:
            logger.warning("No rules found.")
            return

        logger.info(f"Found {len(all_responses)} API responses total.")
        logger.info(f"Found {len(all_rules)} individual rules total.")

        # Save individual rule details with search filters
        logger.info("Saving individual rule details...")
        saved_rules = []
        for rule in all_rules:
            rule_id = rule["id"]
            rule_name = rule.get("name", "Name not found")
            description = rule.get("description", "No description, please update")
            search_outcome = rule.get("search", {}).get("outcome", "Not found")
            search_filter = rule.get("search", {}).get("filter", "Not found")
            last_updated_on = rule.get("last_updated_on", "Not found")
            created_on = rule.get("created_on", "Not found")
            status = rule.get("status", "Not found")
            
            # Create individual rule file with all details including search filter
            # Sanitize rule name for filename (remove special characters)
            from utils.validators import sanitize_filename
            safe_rule_name = sanitize_filename(rule_name)
            
            # Create filename with rule name (no date in filename since it's in folder)
            rule_filename = os.path.join(EXPORT_DIR, f"{safe_rule_name}_{rule_id}.json")

            if save_json(rule_filename, rule):
                logger.info(f"Rule saved: {rule_id} ({rule_name})")
                # Verify file was actually created
                if os.path.exists(rule_filename):
                    file_size = os.path.getsize(rule_filename)
                    logger.info(f"  File size: {file_size} bytes")
                    saved_rules.append({
                        "rule_id": rule_id,
                        "rule_name": rule_name,
                        "description": description,
                        "search_outcome": search_outcome,
                        "search_filter": search_filter,
                        "created_on": created_on,
                        "last_updated_on": last_updated_on,
                        "status": status,
                        "filename": os.path.basename(rule_filename),
                        "file_size": file_size,
                        "timestamp": current_time
                    })
                else:
                    logger.warning(f"  File not found after save attempt")
            else:
                logger.error(f"Failed to save rule: {rule_id}")

        # Create backup summary file
        backup_summary = {
            "backup_timestamp": current_time,
            "backup_date": datetime.now().isoformat(),
            "total_rules_found": len(all_rules),
            "total_api_responses": len(all_responses),
            "saved_rules": saved_rules,
            "export_directory": EXPORT_DIR,
            "filter_used": filter
        }
        
        summary_filename = os.path.join(EXPORT_DIR, f"_backup_summary_{current_time}.json")
        if save_json(summary_filename, backup_summary):
            logger.info(f"Backup summary saved: {summary_filename}")
        else:
            logger.error(f"Failed to save backup summary")

        logger.info(f"Backup completed at {datetime.now().isoformat()}")
        logger.info(f"Total rules processed: {len(all_rules)}")
        logger.info(f"Total files saved: {len(saved_rules) + len(all_responses)}")

    except Exception as e:
        logger.error(f"Error during backup process: {str(e)}")
        logger.error(f"Backup process failed: {type(e).__name__}: {str(e)}")
        
if __name__ == "__main__":
    # Get credentials from environment variables (recommended approach)
    CLIENT_ID = os.getenv("FALCON_CLIENT_ID")
    CLIENT_SECRET = os.getenv("FALCON_CLIENT_SECRET")
    CLOUD_REGION = os.getenv("FALCON_CLOUDREGION", "us-2")

    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: FALCON_CLIENT_ID and FALCON_CLIENT_SECRET environment variables must be set.")
        print("Please set these environment variables before running the script.")
        print("Optional: Set FALCON_CLOUD_REGION (default: us-2)")
        print("Optional: Set BACKUP_FILTER (default: *)")
        exit(1)

    backup_filter = os.getenv("BACKUP_FILTER", "*")
    backup_all_correlation_rules(CLIENT_ID, CLIENT_SECRET, CLOUD_REGION, backup_filter)

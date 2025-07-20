#!/usr/bin/env python3
"""
Backup cleanup utility for CrowdStrike Correlation Rules Backup Tool
"""
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Clean up old backup directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --days 30 --dry-run    # Show what would be deleted
  %(prog)s --days 30              # Delete backups older than 30 days
  %(prog)s --days 7               # Delete backups older than 7 days
        """
    )
    
    parser.add_argument(
        '--days',
        type=int,
        required=True,
        help='Delete backups older than this many days'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be deleted without actually deleting'
    )
    
    parser.add_argument(
        '--backup-dir',
        default='correlation_rules_backups',
        help='Backup directory to clean (default: correlation_rules_backups)'
    )
    
    return parser.parse_args()

def is_valid_backup_directory(dir_path):
    """Check if directory is a valid backup directory"""
    try:
        # Check if it's a date-based directory (YYYY-MM-DD format)
        dir_name = os.path.basename(dir_path)
        datetime.strptime(dir_name, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_backup_directories(backup_root):
    """Get list of backup directories"""
    if not os.path.exists(backup_root):
        print(f"Backup directory '{backup_root}' does not exist")
        return []
    
    backup_dirs = []
    for item in os.listdir(backup_root):
        item_path = os.path.join(backup_root, item)
        if os.path.isdir(item_path) and is_valid_backup_directory(item_path):
            backup_dirs.append(item_path)
    
    return backup_dirs

def should_delete_directory(dir_path, days_old):
    """Check if directory should be deleted based on age"""
    try:
        dir_name = os.path.basename(dir_path)
        backup_date = datetime.strptime(dir_name, '%Y-%m-%d')
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        return backup_date < cutoff_date
    except ValueError:
        return False

def delete_directory(dir_path):
    """Safely delete a directory and its contents"""
    try:
        import shutil
        shutil.rmtree(dir_path)
        print(f"Deleted: {dir_path}")
        return True
    except Exception as e:
        print(f"Error deleting {dir_path}: {e}")
        return False

def main():
    """Main cleanup function"""
    args = parse_arguments()
    
    if args.days < 1:
        print("Error: Days must be at least 1")
        sys.exit(1)
    
    backup_dirs = get_backup_directories(args.backup_dir)
    
    if not backup_dirs:
        print(f"No backup directories found in '{args.backup_dir}'")
        return
    
    # Sort directories by date (oldest first)
    backup_dirs.sort()
    
    to_delete = []
    to_keep = []
    
    for dir_path in backup_dirs:
        if should_delete_directory(dir_path, args.days):
            to_delete.append(dir_path)
        else:
            to_keep.append(dir_path)
    
    print(f"Found {len(backup_dirs)} backup directories")
    print(f"Will keep {len(to_keep)} directories")
    print(f"Will delete {len(to_delete)} directories")
    
    if to_delete:
        print("\nDirectories to be deleted:")
        for dir_path in to_delete:
            dir_name = os.path.basename(dir_path)
            print(f"  - {dir_name}")
        
        if args.dry_run:
            print(f"\nDRY RUN: Would delete {len(to_delete)} directories")
            print("Run without --dry-run to actually delete")
        else:
            print(f"\nDeleting {len(to_delete)} directories...")
            deleted_count = 0
            for dir_path in to_delete:
                if delete_directory(dir_path):
                    deleted_count += 1
            
            print(f"Successfully deleted {deleted_count} directories")
    else:
        print("No directories need to be deleted")
    
    if to_keep:
        print(f"\nKeeping {len(to_keep)} directories:")
        for dir_path in to_keep:
            dir_name = os.path.basename(dir_path)
            print(f"  - {dir_name}")

if __name__ == "__main__":
    main()

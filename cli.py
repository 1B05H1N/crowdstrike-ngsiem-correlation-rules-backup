#!/usr/bin/env python3
"""
Command-line interface for the CrowdStrike Correlation Rules Backup Tool
"""
import os
import sys
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from utils.logger import setup_logger, get_log_filename
from utils.validators import validate_api_credentials, validate_directory_path, ValidationError
from tools.correlation_rules_backup import backup_all_correlation_rules

# Load environment variables from .env file if it exists
load_dotenv()

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """CrowdStrike Correlation Rules Backup Tool"""
    pass

@cli.command()
@click.option('--client-id', envvar='FALCON_CLIENT_ID', help='CrowdStrike API Client ID')
@click.option('--client-secret', envvar='FALCON_CLIENT_SECRET', help='CrowdStrike API Client Secret')
@click.option('--cloud-region', envvar='FALCON_CLOUDREGION', default='us-2', help='CrowdStrike Cloud Region')
@click.option('--backup-filter', envvar='BACKUP_FILTER', default='*', help='Filter for correlation rules (default: *)')
@click.option('--output-dir', default='correlation_rules_backups', help='Output directory for backups')
@click.option('--log-file', help='Log file path (optional)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--dry-run', is_flag=True, help='Validate credentials without performing backup')
def backup(client_id: str, client_secret: str, cloud_region: str, backup_filter: str, output_dir: str, 
           log_file: Optional[str], verbose: bool, dry_run: bool):
    """Backup all correlation rules from CrowdStrike Falcon"""
    
    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    if not log_file:
        log_file = get_log_filename()
    
    logger = setup_logger(log_file=log_file, level=log_level)
    
    try:
        # Display welcome message
        console.print(Panel.fit(
            "[bold blue]CrowdStrike Correlation Rules Backup Tool[/bold blue]\n"
            "Backing up correlation rules from CrowdStrike Falcon API",
            title="Backup Tool"
        ))
        
        # Validate credentials
        if not client_id or not client_secret:
            console.print("[red]Error: Missing API credentials[/red]")
            console.print("Please provide FALCON_CLIENT_ID and FALCON_CLIENT_SECRET")
            console.print("You can set them as environment variables or use --client-id and --client-secret options")
            sys.exit(1)
        
        # Validate output directory
        try:
            validate_directory_path(output_dir)
        except ValidationError as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)
        
        # Test API credentials
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Validating API credentials...", total=None)
            
            try:
                validate_api_credentials(client_id, client_secret)
                progress.update(task, description="API credentials validated")
            except ValidationError as e:
                progress.update(task, description="API credentials invalid")
                console.print(f"[red]Error: {str(e)}[/red]")
                sys.exit(1)
        
        if dry_run:
            console.print("[green]Dry run completed successfully![/green]")
            console.print("Credentials are valid and ready for backup.")
            console.print(f"Backup filter: {backup_filter}")
            return
        
        # Perform backup
        console.print(f"\n[bold]Starting backup to: {output_dir}[/bold]")
        console.print(f"[bold]Using filter: {backup_filter}[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Backing up correlation rules...", total=None)
            
            # Call the backup function
            backup_all_correlation_rules(client_id, client_secret, cloud_region, backup_filter)
            
            progress.update(task, description="Backup completed successfully!")
        
        # Display summary
        console.print("\n[bold green]Backup Summary:[/bold green]")
        summary_table = Table(show_header=True, header_style="bold magenta")
        summary_table.add_column("Item", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Output Directory", output_dir)
        summary_table.add_row("Log File", log_file)
        summary_table.add_row("Cloud Region", cloud_region)
        summary_table.add_row("Backup Filter", backup_filter)
        summary_table.add_row("Status", "Completed")
        
        console.print(summary_table)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Backup interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {str(e)}[/red]")
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)

@cli.command()
def status():
    """Check the status of your configuration"""
    console.print(Panel.fit(
        "[bold blue]Configuration Status[/bold blue]",
        title="Status Check"
    ))
    
    # Check environment variables
    status_table = Table(show_header=True, header_style="bold magenta")
    status_table.add_column("Setting", style="cyan")
    status_table.add_column("Value", style="green")
    status_table.add_column("Status", style="yellow")
    
    # Check credentials
    client_id = os.getenv('FALCON_CLIENT_ID')
    client_secret = os.getenv('FALCON_CLIENT_SECRET')
    cloud_region = os.getenv('FALCON_CLOUDREGION', 'us-2')
    backup_filter = os.getenv('BACKUP_FILTER', '*')
    
    status_table.add_row(
        "FALCON_CLIENT_ID", 
        client_id if client_id else "Not set",
        "Set" if client_id else "Missing"
    )
    
    status_table.add_row(
        "FALCON_CLIENT_SECRET", 
        "***" if client_secret else "Not set",
        "Set" if client_secret else "Missing"
    )
    
    status_table.add_row(
        "FALCON_CLOUDREGION", 
        cloud_region,
        "Set"
    )
    
    status_table.add_row(
        "BACKUP_FILTER", 
        backup_filter,
        "Set"
    )
    
    console.print(status_table)
    
    # Check if .env file exists
    env_file = Path('.env')
    if env_file.exists():
        console.print(f"\n[green].env file found: {env_file}[/green]")
    else:
        console.print(f"\n[yellow]No .env file found. Consider creating one for easier configuration.[/yellow]")

@cli.command()
def setup():
    """Interactive setup for the backup tool"""
    console.print(Panel.fit(
        "[bold blue]Interactive Setup[/bold blue]\n"
        "This will help you configure the backup tool",
        title="Setup"
    ))
    
    # Get API credentials
    console.print("\n[bold]Step 1: API Credentials[/bold]")
    client_id = click.prompt("Enter your CrowdStrike API Client ID")
    client_secret = click.prompt("Enter your CrowdStrike API Client Secret", hide_input=True)
    cloud_region = click.prompt("Enter your CrowdStrike Cloud Region", default="us-2")
    
    # Get backup filter with explanation
    console.print("\n[bold]Step 2: Backup Filter[/bold]")
    console.print("The backup filter determines which correlation rules to backup:")
    console.print("• \"*\" = Backup all rules (default)")
    console.print("• \"user_id:!'user@example.com'\" = Exclude rules by user")
    console.print("• \"status:'enabled'\" = Only backup enabled rules")
    console.print("• \"name:'*test*'\" = Only backup rules with 'test' in name")
    console.print("• \"user_id:'admin@example.com'+status:'enabled'\" = Multiple conditions")
    
    backup_filter = click.prompt(
        "Enter backup filter", 
        default="*"
    )
    
    # Create .env file
    env_content = f"""# CrowdStrike API Configuration
FALCON_CLIENT_ID={client_id}
FALCON_CLIENT_SECRET={client_secret}
FALCON_CLOUDREGION={cloud_region}
BACKUP_FILTER={backup_filter}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    console.print(f"\n[green]Configuration saved to .env file[/green]")
    console.print(f"[green]Backup filter set to: {backup_filter}[/green]")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Run 'python cli.py status' to verify your configuration")
    console.print("2. Run 'python cli.py backup' to start a backup")
    console.print("3. Run 'python cli.py backup --dry-run' to test without backing up")

if __name__ == '__main__':
    cli() 
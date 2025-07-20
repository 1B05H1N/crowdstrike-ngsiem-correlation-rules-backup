# CrowdStrike Correlation Rules Backup Tool

A Python tool for backing up CrowdStrike correlation rules using the Falcon API.

## About FalconPy

This tool uses [FalconPy](https://www.falconpy.io/Home.html), the CrowdStrike Falcon API Software Development Kit. FalconPy is a collection of Python classes that abstract CrowdStrike Falcon OAuth2 API interaction, removing duplicative code and allowing developers to focus on just the logic of their solution requirements.

### FalconPy SDK Contents

FalconPy provides two distinct methods for interacting with the CrowdStrike Falcon OAuth2 API:

| Service Classes | Uber Class |
|----------------|------------|
| Representing a single service collection, Service Classes have methods defined for every available operation within that specific service collection. | A single harness for interacting with the entire API, the Uber Class can interact with every available operation within every service collection. |

This tool specifically uses the **Correlation Rules Service Class** to interact with CrowdStrike Falcon Correlation Rules functionality.

## Features

- Automated backup of all correlation rules
- Date-based organization of backups
- Detailed backup summaries
- Secure credential management via environment variables
- Individual rule files with metadata
- Progress tracking and logging
- Flexible filtering using Falcon Query Language (FQL)

## Security

### Git Repository Security

**Important**: This repository is configured to exclude sensitive files from version control:

- **Backup files** (`correlation_rules_backups/`) - Never committed to git
- **Log files** (`logs/`) - Never committed to git  
- **Environment files** (`.env`) - Never committed to git
- **Credentials** - Never hardcoded in source code

All backup data and logs are stored locally and excluded from git via `.gitignore`. This ensures:

- **No sensitive data** in version control  
- **No API credentials** exposed  
- **No backup files** in repository  
- **No logs** containing sensitive information  

### Environment Configuration

Create a `.env` file in the project root:
```bash
# CrowdStrike API Configuration
FALCON_CLIENT_ID=your_client_id_here
FALCON_CLIENT_SECRET=your_client_secret_here
FALCON_CLOUDREGION=us-2
BACKUP_FILTER=*
```

**Never commit your `.env` file to git!**

## Prerequisites

- Python 3.7+ (for Python installation)
- Docker and Docker Compose (for Docker installation)
- CrowdStrike Falcon API credentials
- Virtual environment (recommended for Python installation)

## Installation

### Quick Start (Recommended)

For the fastest setup, run the quick start script:

```bash
./quick_start.sh
```

This will:
- Check Python version
- Create virtual environment
- Install dependencies
- Create .env file from template
- Run compatibility tests
- Provide next steps

### Option 1: Direct Python Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd correlation_rules_backup_tool
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Package Installation

Install as a Python package:

```bash
pip install -e .
```

This will make the tool available as `crowdstrike-backup` command.

### Option 3: Docker Deployment

#### Using Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd correlation_rules_backup_tool
   ```

2. **Build and run with Docker Compose:**
   ```bash
   # Setup configuration
   docker-compose --profile setup up
   
   # Check status
   docker-compose --profile status up
   
   # Run backup
   docker-compose --profile backup up
   ```

#### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t crowdstrike-backup .
   ```

2. **Run the container:**
   ```bash
   # Setup
   docker run -it --rm -v $(pwd)/.env:/app/.env crowdstrike-backup setup
   
   # Check status
   docker run -it --rm -v $(pwd)/.env:/app/.env crowdstrike-backup status
   
   # Run backup
   docker run -it --rm \
     -v $(pwd)/correlation_rules_backups:/app/correlation_rules_backups \
     -v $(pwd)/logs:/app/logs \
     -v $(pwd)/.env:/app/.env:ro \
     crowdstrike-backup backup
   ```

### Option 4: Using Makefile

If you have `make` installed:

```bash
# Install dependencies
make install

# Run tests
make test

# Interactive setup
make setup

# Check status
make status

# Run backup
make backup

# Clean up
make clean
```

## Configuration

Set your CrowdStrike API credentials as environment variables:

```bash
export FALCON_CLIENT_ID="your_client_id"
export FALCON_CLIENT_SECRET="your_client_secret"
export FALCON_CLOUDREGION="us-2"  # Optional, defaults to us-2
export BACKUP_FILTER="*"  # Optional, defaults to "*" (all rules)
```

### Filter Options

The `BACKUP_FILTER` environment variable allows you to specify which correlation rules to backup using Falcon Query Language (FQL):

- `"*"` - Backup all rules (default)
- `"user_id:!'user@crowdstrike.com'"` - Exclude rules created by specific user
- `"status:'enabled'"` - Only backup enabled rules
- `"name:'*test*'"` - Only backup rules with "test" in the name
- `"user_id:'admin@example.com'+status:'enabled'"` - Multiple conditions (AND logic)

**Working Filter Examples:**
```bash
# Exclude specific user
BACKUP_FILTER="user_id:!'user@crowdstrike.com'" python cli.py backup

# Only enabled rules
BACKUP_FILTER="status:'enabled'" python cli.py backup

# Command line option
python cli.py backup --backup-filter "user_id:!'user@crowdstrike.com'"
```

For more filter options, refer to the [CrowdStrike API documentation](https://falconpy.io/Service-Collections/Correlation-Rules.html) and [Falcon Query Language](https://www.falconpy.io/Usage/Falcon-Query-Language.html).

## Usage Instructions

### Python Usage

#### Step 1: Setup Configuration

**Interactive Setup:**
```bash
python cli.py setup
```
This will prompt you for:
- CrowdStrike API Client ID
- CrowdStrike API Client Secret
- CrowdStrike Cloud Region (default: us-2)
- Backup filter (default: *)

**Manual Setup:**
Create a `.env` file in the project root:
```bash
# CrowdStrike API Configuration
FALCON_CLIENT_ID=your_client_id_here
FALCON_CLIENT_SECRET=your_client_secret_here
FALCON_CLOUDREGION=us-2
BACKUP_FILTER=*
```

#### Step 2: Verify Configuration

```bash
python cli.py status
```

This will show:
- API credentials status
- Environment variables
- Configuration file status

#### Step 3: Test Credentials

```bash
python cli.py backup --dry-run
```

This validates your credentials without performing a backup.

#### Step 4: Run Backup

```bash
# Basic backup
python cli.py backup

# Verbose logging
python cli.py backup --verbose

# Custom output directory
python cli.py backup --output-dir /path/to/backups

# Custom log file
python cli.py backup --log-file /path/to/logs/backup.log
```

### Docker Usage

#### Step 1: Setup Configuration

**Using Docker Compose:**
```bash
# Interactive setup
docker-compose --profile setup up

# This will create a .env file with your configuration
```

**Using Docker directly:**
```bash
# Interactive setup
docker run -it --rm -v $(pwd)/.env:/app/.env crowdstrike-backup setup
```

#### Step 2: Verify Configuration

```bash
# Using Docker Compose
docker-compose --profile status up

# Using Docker directly
docker run -it --rm -v $(pwd)/.env:/app/.env crowdstrike-backup status
```

#### Step 3: Test Credentials

```bash
# Using Docker Compose
docker-compose run --rm crowdstrike-backup backup --dry-run

# Using Docker directly
docker run -it --rm \
  -v $(pwd)/.env:/app/.env:ro \
  crowdstrike-backup backup --dry-run
```

#### Step 4: Run Backup

```bash
# Using Docker Compose
docker-compose --profile backup up

# Using Docker directly
docker run -it --rm \
  -v $(pwd)/correlation_rules_backups:/app/correlation_rules_backups \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env:ro \
  crowdstrike-backup backup
```

### Advanced Usage

#### Custom Filters

**Python:**
```bash
# Backup only enabled rules
BACKUP_FILTER="status:'enabled'" python cli.py backup

# Exclude specific user's rules
BACKUP_FILTER="user_id:!'user@crowdstrike.com'" python cli.py backup

# Command line option
python cli.py backup --backup-filter "user_id:!'user@crowdstrike.com'"

# Multiple conditions
BACKUP_FILTER="user_id:'admin@example.com'+status:'enabled'" python cli.py backup
```

**Docker:**
```bash
# Using environment variable
docker run -it --rm \
  -v $(pwd)/correlation_rules_backups:/app/correlation_rules_backups \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env:ro \
  -e BACKUP_FILTER="status:'enabled'" \
  crowdstrike-backup backup
```

#### Scheduled Backups

**Using Cron (Linux/macOS):**
```bash
# Add to crontab -e
0 2 * * * cd /path/to/tool && python cli.py backup >> /var/log/crowdstrike-backup.log 2>&1
```

**Using Docker with Cron:**
```bash
# Create a cron job that runs the Docker container
0 2 * * * docker run --rm \
  -v /path/to/backups:/app/correlation_rules_backups \
  -v /path/to/logs:/app/logs \
  -v /path/to/.env:/app/.env:ro \
  crowdstrike-backup backup
```

## Output

The script creates:
- Date-based backup directories (`correlation_rules_backups/YYYY-MM-DD/`)
- Individual rule JSON files
- API response files
- Backup summary with metadata

### Backup Structure

```
correlation_rules_backups/
└── 2025-07-19/
    ├── _backup_summary_143022.json
    ├── api_response_offset_0_143022.json
    ├── api_response_offset_500_143022.json
    ├── Rule_Name_1_rule_id_123.json
    ├── Rule_Name_2_rule_id_456.json
    └── ...
```

## Project Structure

```
correlation_rules_backup_tool/
├── README.md
├── requirements.txt
├── config.py
├── cli.py
├── setup.py
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── LICENSE
├── CHANGELOG.md
├── SECURITY.md
├── test_compatibility.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── validators.py
└── tools/
    ├── correlation_rules_backup.py
    └── correlation_rules_backups/
        └── YYYY-MM-DD/
            ├── _backup_summary_HHMMSS.json
            ├── api_response_offset_0_HHMMSS.json
            └── rule_name_rule_id.json
```

## API Reference

This tool uses the CrowdStrike FalconPy library to interact with the CrowdStrike API. For detailed information about the Correlation Rules API endpoints and methods, refer to the [FalconPy Correlation Rules Documentation](https://www.falconpy.io/Service-Collections/Correlation-Rules.html).

### FalconPy Service Collections

FalconPy provides 94 Service Classes that provide an interface to individual service collections within the CrowdStrike Falcon OAuth2 API. This tool specifically uses the Correlation Rules service collection.

## Troubleshooting

### Common Issues

**Authentication Errors:**
```bash
# Check credentials
python cli.py status

# Test with dry-run
python cli.py backup --dry-run
```

**Network Issues:**
- Verify internet connectivity
- Check firewall settings
- Ensure CrowdStrike API endpoints are accessible

**Permission Errors:**
```bash
# Check directory permissions
ls -la correlation_rules_backups/
ls -la logs/

# Fix permissions if needed
chmod 755 correlation_rules_backups/
chmod 755 logs/
```

**Docker Issues:**
```bash
# Check Docker is running
docker --version
docker-compose --version

# Rebuild image if needed
docker-compose build --no-cache
```

### Debug Mode

**Python:**
```bash
python cli.py backup --verbose
```

**Docker:**
```bash
docker run -it --rm \
  -v $(pwd)/correlation_rules_backups:/app/correlation_rules_backups \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env:ro \
  crowdstrike-backup backup --verbose
```

## Testing

Run the compatibility test to verify your environment:

```bash
python test_compatibility.py
```

This will check:
- Python version compatibility
- Required package availability
- Local module imports
- Configuration setup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Security

Please review [SECURITY.md](SECURITY.md) for security best practices and vulnerability reporting procedures.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a complete list of changes and version history. 
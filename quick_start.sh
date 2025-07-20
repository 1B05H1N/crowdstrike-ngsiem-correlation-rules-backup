#!/bin/bash

# CrowdStrike Correlation Rules Backup Tool - Quick Start Script
# This script helps you get started quickly with the backup tool

set -e

echo "CrowdStrike Correlation Rules Backup Tool - Quick Start"
echo "======================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "INFO: Python $PYTHON_VERSION detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "INFO: Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "INFO: Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "INFO: Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "INFO: Creating .env file from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "SUCCESS: .env file created from env.example"
        echo "WARNING: Please edit .env file with your CrowdStrike API credentials"
    else
        echo "INFO: Creating basic .env file..."
        cat > .env << EOF
# CrowdStrike API Configuration
FALCON_CLIENT_ID=your_client_id_here
FALCON_CLIENT_SECRET=your_client_secret_here
FALCON_CLOUDREGION=us-2
BACKUP_FILTER=*
EOF
        echo "SUCCESS: Basic .env file created"
        echo "WARNING: Please edit .env file with your CrowdStrike API credentials"
    fi
else
    echo "INFO: .env file already exists"
fi

# Run compatibility test
echo "INFO: Running compatibility test..."
python test_compatibility.py

echo ""
echo "SUCCESS: Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your CrowdStrike API credentials"
echo "2. Run: python cli.py setup"
echo "3. Run: python cli.py status"
echo "4. Run: python cli.py backup --dry-run"
echo "5. Run: python cli.py backup"
echo ""
echo "For Docker usage:"
echo "1. docker-compose --profile setup up"
echo "2. docker-compose --profile status up"
echo "3. docker-compose --profile backup up"
echo ""
echo "For help: python cli.py --help" 
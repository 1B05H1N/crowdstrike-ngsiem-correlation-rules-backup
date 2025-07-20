# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of CrowdStrike Correlation Rules Backup Tool
- Command-line interface with interactive setup
- Environment variable support for API credentials and filters
- Falcon Query Language (FQL) filtering capabilities
- Date-based backup organization
- Comprehensive logging and progress tracking
- Backup summary with metadata
- Individual rule file export
- Security documentation and best practices
- Compatibility testing script

### Features
- Support for CrowdStrike Falcon API via FalconPy
- Flexible filtering using BACKUP_FILTER environment variable
- Interactive CLI with setup, status, and backup commands
- Dry-run capability for testing without performing backup
- Verbose logging options
- Automatic backup directory creation with date-based organization
- JSON export of individual correlation rules
- Backup summary with statistics and metadata

### Technical Details
- Python 3.7+ compatibility
- FalconPy SDK integration
- Environment variable configuration
- Comprehensive error handling
- Logging with file rotation
- Input validation and sanitization
- Cross-platform compatibility

## [1.0.0] - 2025-07-19

### Added
- Initial release
- Basic backup functionality
- CLI interface
- Configuration management
- Logging system
- Error handling
- Documentation 
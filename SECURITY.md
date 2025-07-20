# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Best Practices

### API Credentials
- **NEVER commit API credentials to version control**
- Use environment variables for sensitive data
- Store credentials in `.env` files (excluded from git)
- Use CrowdStrike API Client ID and Secret only
- Rotate credentials regularly

### Environment Configuration
- Use `.env` files for local development (ensure they're in `.gitignore`)
- Never hardcode credentials in source code
- Use `env.example` as a template for required variables
- Validate all environment variables before use

### File Security
- Backup files are stored locally in `correlation_rules_backups/`
- Log files are stored in `logs/` directory
- All sensitive files are excluded via `.gitignore`
- No credentials are logged or exposed in output

### Network Security
- All API calls use HTTPS/TLS
- Credentials are transmitted securely via CrowdStrike API
- No local network services are exposed
- All connections use official CrowdStrike endpoints

### Code Security
- No use of `eval()` or `exec()` functions
- No direct shell command execution
- Input validation on all user inputs
- Proper error handling without exposing sensitive data
- Logging excludes sensitive information

### Docker Security
- No secrets baked into Docker images
- Environment variables passed at runtime
- Read-only mounts for configuration files
- Non-root user in containers (when possible)

### Recent Security Cleanup
- **COMPLETED**: Removed exposed API credentials from repository
- **COMPLETED**: Cleared entire git history to remove any trace of secrets
- **COMPLETED**: Started fresh repository with clean commit history
- **COMPLETED**: Verified all sensitive files are properly excluded

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** create a public issue
2. Email security details to: 1B05H1N@pm.me
3. Include detailed steps to reproduce
4. Provide any relevant logs or error messages
5. Allow time for assessment and response

## Security Checklist

- [x] No hardcoded credentials in source code
- [x] Environment variables used for all sensitive data
- [x] `.env` files excluded from version control
- [x] Input validation implemented
- [x] No dangerous functions used (`eval`, `exec`, etc.)
- [x] Secure API communication (HTTPS/TLS)
- [x] Proper error handling without data exposure
- [x] Logging excludes sensitive information
- [x] Git history cleared of any secrets
- [x] All sensitive files properly ignored

## Environment Variables Security

Required environment variables:
- `FALCON_CLIENT_ID` - CrowdStrike API Client ID
- `FALCON_CLIENT_SECRET` - CrowdStrike API Client Secret
- `FALCON_CLOUDREGION` - CrowdStrike Cloud Region
- `BACKUP_FILTER` - Optional filter for correlation rules

**IMPORTANT**: These should never be committed to version control!

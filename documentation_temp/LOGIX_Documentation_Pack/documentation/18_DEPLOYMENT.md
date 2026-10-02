# Deployment

## Current Local Architecture
```text
Windows
  |
  +-- Python environment
  +-- MySQL
  +-- Streamlit
  +-- Power BI Desktop
  +-- Excel
```

## Environment Variables
Database credentials are stored in local `.env` files and excluded from Git.

```text
LOGIX_DB_HOST=localhost
LOGIX_DB_PORT=3306
LOGIX_DB_USER=root
LOGIX_DB_PASSWORD=YOUR_MYSQL_PASSWORD
LOGIX_DB_NAME=logix
```

## Deployment Roadmap
1. Validate locally
2. Document database setup
3. Document environment variables
4. Prepare production database strategy
5. Deploy Streamlit
6. Publish Power BI through an appropriate workspace if required

No production deployment is claimed unless separately verified.

# GitHub Actions

Simple CI/CD workflow for the Python Flask webhook service.

## Workflow

- **Python Webhook CI** (`ci.yml`): Tests the Flask webhook service
  - Validates Python syntax
  - Tests Flask app imports
  - Tests webhook endpoints
  - Runs security checks with Safety and Bandit

## Triggers

- Push to `main` branch
- Pull requests to `main` branch

## Requirements

No additional secrets required - the workflow uses only built-in GitHub Actions functionality.

## Status Badge

Add this to your main README.md:

```markdown
[![Python Webhook CI](https://github.com/username/downtime_caller/workflows/Python%20Webhook%20CI/badge.svg)](https://github.com/username/downtime_caller/actions)
```
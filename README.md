# Bayers Hackthon Dev - Python App with CI DevSecOps

This repository contains a simple Python service and a GitHub Actions pipeline that includes:

- CI build and test
- SonarQube scan with quality gate
- Trivy vulnerability scan
- OWASP Dependency-Check scan
- SBOM generation (SPDX)

## App

Endpoints:

- `GET /` → health status
- `GET /add/<a>/<b>` → adds two integers

Run locally:

```bash
python app/main.py
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## CI/CD workflow

Workflow file: `.github/workflows/ci-devsecops.yml`

### Required GitHub configuration for SonarQube

Add these in your repository settings:

- Repository variable: `SONAR_HOST_URL` (example: `https://sonarqube.your-company.com`)
- Repository secret: `SONAR_TOKEN`

If these are missing, the SonarQube job is skipped while all other checks continue.

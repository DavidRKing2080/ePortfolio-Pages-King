# Security & Compliance Crawler

A lightweight dependency scanner that parses Python and Node lockfiles, queries the [OSV database](https://osv.dev/) for known vulnerabilities, and generates human-readable and machine-readable reports.  

Designed to integrate seamlessly into CI/CD pipelines.

---

## Features
- Parses common dependency manifests:
  - Python: `requirements.txt`, `poetry.lock`
  - JavaScript: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- Queries [OSV](https://osv.dev) for CVEs and CVSS scores
- Outputs:
  - `findings.json` (machine-readable JSON report)
  - Console summary table
- CI-friendly:
  - Exits with non-zero status if CVSS ≥ 7 vulnerabilities are found
- Automation-ready:
  - GitHub Actions workflow provided
  - Docker image for portable runs
- Optional Slack alerts for high/critical findings

---

## Tech Stack
- Python 3.11
- Argparse
- OSV API
- Docker
- GitHub Actions

---

## Quick Start

### 1. Clone & set up
```bash
git clone https://github.com/YourUser/security-crawler.git
cd security-crawler
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt


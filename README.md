# Bayers Hackthon Dev - Python App with CI DevSecOps

This repository contains a simple Python service and a GitHub Actions pipeline implementing **shift-left security** and **continuous code quality** checks.

The goal is not only to build and test the app, but to continuously answer:

- Is the code maintainable and reliable?
- Are we introducing known vulnerabilities through dependencies or base images?
- Are we aligning with OWASP guidance?
- Can developers quickly understand and triage findings from reports?

---

## Why these security checks are needed

Modern software risk comes from multiple layers:

1. **Application code risk** (bugs, security anti-patterns, maintainability issues)
2. **Open-source dependency risk** (CVE exposure, outdated libraries)
3. **Container/base image risk** (OS package vulnerabilities)
4. **Configuration and governance risk** (missing quality gates, weak visibility)

A single scanner cannot cover all these layers. That is why this pipeline combines **SonarQube**, **Trivy**, **OWASP Dependency-Check**, and **SBOM generation**.

---

## Security and quality controls in this repo

### 1) Code Analysis (SonarQube)

**What it does**

- Static analysis of source code for:
  - Bugs and code smells
  - Security hotspots and vulnerabilities
  - Maintainability debt
  - Test coverage trends (if coverage reports are supplied)

**Why it is needed**

- Prevents bad patterns from reaching production.
- Enforces a measurable quality gate before merge/deploy.
- Gives a long-term view of technical debt and code health.

**Best for**

- Developer feedback during pull requests
- Governance via Quality Gates

---

### 2) Trivy (Filesystem + Dependency + Container/Image scanning)

**What it does**

- Scans project filesystem (`fs`) and/or container images for:
  - OS package CVEs
  - Language dependency CVEs
  - Misconfigurations (depending on mode)
  - Secrets (depending on mode)

**Why Trivy `fs` scan is needed**

- Catches vulnerable dependencies directly from source/manifests before image build.
- Fast local/CI feedback loop.
- Helps detect vulnerabilities even when no container image has been produced yet.

**Best for**

- Early dependency security checks
- Broad vulnerability visibility across artifacts

---

### 3) OWASP Dependency-Check

**What it does**

- Identifies vulnerable third-party libraries by correlating dependencies with known CVEs/NVD data.

**Why it is needed in addition to Trivy**

- Provides another detection engine and report style for dependency risk.
- Useful for compliance-oriented pipelines and audit-friendly reports.
- Defense-in-depth: different tools sometimes catch different issues or metadata contexts.

**Best for**

- Dependency governance and audit trails
- Structured vulnerability reporting for security review

---

### 4) SBOM Generation (SPDX)

**What it does**

- Produces a Software Bill of Materials listing included components and versions.

**Why it is needed**

- Improves supply-chain transparency.
- Speeds incident response (e.g., “Are we affected by CVE-X?”).
- Supports enterprise/customer compliance requirements.

---

## OWASP alignment (what risks these tools help reduce)

This stack contributes to OWASP risk reduction (especially OWASP Top 10 style categories), for example:

- **A06:2021 – Vulnerable and Outdated Components**
  - Trivy + Dependency-Check + SBOM are key controls.
- **A08:2021 – Software and Data Integrity Failures**
  - SBOM and controlled CI checks improve integrity and traceability.
- **A05:2021 – Security Misconfiguration**
  - Trivy can surface configuration weaknesses (mode-dependent).
- **A03:2021 – Injection / Code-level weaknesses**
  - SonarQube helps detect risky code patterns and hotspots early.

> Note: No tool “solves OWASP” alone. Security requires layered controls + human review.

---

## How to read the reports (practical guide)

### A) SonarQube report interpretation

When opening a SonarQube project dashboard, prioritize in this order:

1. **Quality Gate status**
   - Pass/Fail is the merge/deploy decision point.
2. **Security issues and hotspots**
   - Review severity and whether hotspot is truly exploitable.
3. **Reliability issues (bugs)**
   - Focus on high severity first.
4. **Maintainability/code smells**
   - Address high-impact debt and repeated patterns.
5. **New Code vs Overall Code**
   - Prefer strict standards on new code to prevent debt growth.

**Triage tips**

- Fix issues in “New Code” first.
- If marking false positives, always add clear justification comments.
- Track recurring rule violations and add coding standards/tests.

---

### B) Trivy report interpretation

Typical Trivy output includes:

- Package or component name
- Installed version
- Fixed version (if available)
- Severity (CRITICAL/HIGH/MEDIUM/LOW)
- CVE ID and reference links

**Prioritization order**

1. CRITICAL with known fix available
2. HIGH with known fix available
3. Reachable vulnerabilities in runtime dependencies
4. Medium/Low issues based on exposure context

**Decision flow**

- **If fix exists** → upgrade dependency/base image.
- **If no fix** → mitigate (pin safer alternatives, reduce exposure, monitor).
- **If not applicable** → document risk acceptance with evidence.

---

### C) OWASP Dependency-Check report interpretation

Dependency-Check reports usually include:

- Dependency file/component
- Matched CPE/CVE
- CVSS score
- Confidence/suppression context

**How to triage**

1. Validate the vulnerable component is truly used/reachable.
2. Confirm version mapping accuracy (watch for false CPE matches).
3. Patch/upgrade where possible.
4. Use suppressions only with documented reason and expiry review.

---

### D) SBOM usage interpretation

Use SBOM to answer:

- What exact versions are in this build?
- Which services include a vulnerable library?
- Which artifact needs rebuild after a CVE disclosure?

SBOM is most useful when versioned and stored per release artifact.

---

## Suggested remediation SLA model

A simple policy teams can adopt:

- **CRITICAL**: fix or mitigate in 24–72 hours
- **HIGH**: fix in 7 days
- **MEDIUM**: fix in 30 days
- **LOW**: backlog with periodic review

Always adjust by exploitability, internet exposure, and business criticality.

---

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

---

## CI/CD workflow

Workflow file: `.github/workflows/ci-devsecops.yml`

### Required GitHub configuration for SonarQube

Add these in repository settings:

- Repository variable: `SONAR_HOST_URL` (example: `https://sonarqube.your-company.com`)
- Repository secret: `SONAR_TOKEN`

If these are missing, SonarQube analysis can be skipped while other checks continue (based on workflow conditions).

---

## Quick “how to act on findings” checklist

1. Start with failed Quality Gate or highest severity CVEs.
2. Fix items with available patches first.
3. Re-run pipeline to verify closure.
4. Document exceptions (false positive / risk acceptance) with owner + expiry.
5. Track recurring issues and improve coding/dependency policies.

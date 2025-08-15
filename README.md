# Syfe Ultimate Multi-User Parallel Bug Bounty Scanner

**Version:** 1.0  
**Author:** [Anower Hossain Rubel]  
**Date:** 2025-08-16  

---

## Overview

This Python script is a **fully automated, multi-user parallel bug bounty scanner** for Syfe’s authorized environments (UAT / test domains). It is designed to:

- Perform **multi-user parallel fuzzing**.
- Simulate **realistic trade and investment API interactions**.
- Test **JWT manipulation, rate-limit bypass, and edge-case API payloads**.
- Conduct **auth, business logic, and vulnerability scanning** (XSS, SQLi, etc.).
- Generate **Markdown and PDF PoC reports** automatically.

> ⚠️ **Important:** Use ONLY in authorized UAT or testing environments. Unauthorized testing on production may lead to legal consequences.

---

## Features

1. **Multi-User Parallel Execution**  
   Simultaneously tests multiple user tokens for faster coverage.

2. **Realistic Trade Simulation**  
   - Randomized `buy/sell` trades  
   - Varying amounts  
   - Portfolio manipulation  
   - Duplicate order / edge-case simulation

3. **API Fuzzing & Business Logic Testing**  
   - JWT manipulation  
   - Rate-limit bypass attempts  
   - Auth & privilege escalation checks

4. **Recon & Vulnerability Scan (Optional Modules)**  
   - Subdomain discovery (`subfinder`, `amass`)  
   - Directory brute-forcing (`gobuster`)  
   - Port scanning (`nmap`)  
   - Technology fingerprinting (`whatweb`)  
   - XSS scanning (`dalfox`)  
   - SQLi scanning (`sqlmap`)

5. **Automated Reporting**  
   - Markdown report with detailed results  
   - PDF export using `pdfkit`

---

## Requirements

- **Python 3.9+**  
- **Dependencies:**
  ```bash
  pip install aiohttp pdfkit
  sudo apt install wkhtmltopdf
python3 syfe_parallel_scan.py

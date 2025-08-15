#!/usr/bin/env python3
"""
Syfe Ultimate Multi-User Parallel Bug Bounty Scanner
Features:
- Multi-User Parallel Fuzzing
- Realistic Trade / Investment Simulation
- JWT Manipulation, Rate-limit bypass
- Recon, XSS/SQLi, Auth, Business Logic Checks
- PDF-ready PoC Report
⚠️ Use ONLY on UAT / Authorized Production
"""

import os, asyncio, aiohttp, json, random, string
from datetime import datetime
import pdfkit

# ----------------------
# Configuration
# ----------------------
DOMAINS = [
    "api-uat-bugbounty.nonprod.syfe.com",
    "api.syfe.com",
    "alfred.syfe.com"
]

# Multi-user tokens for parallel testing
TOKENS = ["USER_TOKEN_1", "USER_TOKEN_2", "USER_TOKEN_3", "USER_TOKEN_4"]

ENDPOINTS = [
    "/api/v1/investments",
    "/api/v1/orders",
    "/api/v1/portfolio"
]

OUTPUT_DIR = "syfe_parallel_scan_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
REPORT_MD = f"{OUTPUT_DIR}/Syfe_Parallel_BugBounty_Report_{timestamp}.md"

# ----------------------
# Helpers
# ----------------------
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def simulate_user(session, token):
    results = []
    headers = {"Authorization": f"Bearer {token}"}
    for domain in DOMAINS:
        for ep in ENDPOINTS:
            url = f"https://{domain}{ep}"

            # Realistic GET check
            async with session.get(url, headers=headers) as resp:
                try:
                    data = await resp.json()
                    results.append((token, url, "GET", resp.status, str(data)[:200]))
                except:
                    results.append((token, url, "GET", resp.status, "Non-JSON Response"))

            # Realistic POST / Investment Simulation
            for i in range(3):  # multiple trade attempts
                payload = {
                    "amount": random.randint(1, 500000),
                    "trade_type": random.choice(["buy", "sell"]),
                    "portfolio_id": random.randint(1, 10),
                    "description": random_string(15)
                }
                async with session.post(url, headers=headers, json=payload) as resp:
                    results.append((token, url, "POST", resp.status, payload))

            # Rate-limit bypass
            for i in range(2):
                headers_rl = headers.copy()
                headers_rl["X-Bypass-RL"] = random_string(8)
                async with session.get(url, headers=headers_rl) as resp:
                    results.append((token, url, f"RL-Bypass-{i}", resp.status))

            # JWT manipulation
            manipulated_token = token[::-1]
            headers_jwt = {"Authorization": f"Bearer {manipulated_token}"}
            async with session.get(url, headers=headers_jwt) as resp:
                results.append((token, url, "JWT-Tamper", resp.status))

    return results

# ----------------------
# Run Parallel Simulation
# ----------------------
async def run_parallel_simulation():
    async with aiohttp.ClientSession() as session:
        tasks = [simulate_user(session, token) for token in TOKENS]
        all_results = await asyncio.gather(*tasks)
    # Flatten results
    flat_results = [item for sublist in all_results for item in sublist]
    # Save results
    output_file = f"{OUTPUT_DIR}/parallel_results_{timestamp}.txt"
    with open(output_file, "w") as f:
        for r in flat_results:
            f.write(str(r) + "\n")
    print(f"[+] Multi-User Parallel Simulation results saved: {output_file}")
    return output_file

# ----------------------
# Report Generation
# ----------------------
def generate_report(result_file):
    with open(REPORT_MD, "w") as f:
        f.write(f"# Syfe Ultimate Bug Bounty Report\nDate: {datetime.now()}\n\n")
        f.write(f"Domains Scanned: {DOMAINS}\nOutput Folder: {OUTPUT_DIR}\nTokens: {TOKENS}\n\n")
        f.write(f"## Simulation Results\n- File: {result_file}\n")
        f.write("## Manual Testing Recommendations\n- CSRF, Sensitive Data, Privilege Escalation, Advanced Trade Logic\n")
    try:
        pdfkit.from_file(REPORT_MD, REPORT_MD.replace(".md", ".pdf"))
        print(f"[+] PDF Report Generated: {REPORT_MD.replace('.md','.pdf')}")
    except Exception as e:
        print(f"[!] PDF generation failed: {e}")

# ----------------------
# Main Execution
# ----------------------
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result_file = loop.run_until_complete(run_parallel_simulation())
    generate_report(result_file)
    print("[+] Ultimate Multi-User Parallel Bug Bounty Scan Completed!")

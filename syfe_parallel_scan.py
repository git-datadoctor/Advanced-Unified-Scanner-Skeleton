import asyncio
import aiohttp
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ----------------------
# Configuration
# ----------------------
DOMAINS = ["api-uat-bugbounty.nonprod.syfe.com", "api.syfe.com"]
TOKENS = ["USER_TOKEN_1", "USER_TOKEN_2"]
ENDPOINTS = ["/api/v1/investments", "/api/v1/orders"]
OUTPUT_DIR = "syfe_parallel_scan_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ----------------------
# Async API Scanner
# ----------------------
async def test_endpoint(session, domain, endpoint, token):
    url = f"https://{domain}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    async with session.get(url, headers=headers) as resp:
        result = await resp.text()
        return domain, endpoint, resp.status, result[:200]  # first 200 chars

async def run_scan():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for domain in DOMAINS:
            for endpoint in ENDPOINTS:
                for token in TOKENS:
                    tasks.append(test_endpoint(session, domain, endpoint, token))
        results = await asyncio.gather(*tasks)
        return results

# ----------------------
# PDF Report Generation
# ----------------------
def generate_pdf_report(results):
    pdf_file = os.path.join(OUTPUT_DIR, f"Syfe_Parallel_BugBounty_Report_{timestamp}.pdf")
    c = canvas.Canvas(pdf_file, pagesize=letter)
    textobject = c.beginText(50, 750)
    textobject.setFont("Helvetica", 10)

    textobject.textLine(f"Syfe Parallel Bug Bounty Report - {datetime.now()}")
    textobject.textLine("-" * 80)
    textobject.textLine(f"Domains Tested: {DOMAINS}")
    textobject.textLine(f"Endpoints: {ENDPOINTS}")
    textobject.textLine(f"Tokens Used: {TOKENS}")
    textobject.textLine("-" * 80)
    textobject.textLine("Results (status + snippet):")
    textobject.textLine("")

    for domain, endpoint, status, snippet in results:
        textobject.textLine(f"{domain}{endpoint} -> Status: {status}")
        textobject.textLine(f"Response Snippet: {snippet}")
        textobject.textLine("")

    c.drawText(textobject)
    c.save()
    print(f"[+] PDF Report Generated: {pdf_file}")

# ----------------------
# Main
# ----------------------
if __name__ == "__main__":
    results = asyncio.run(run_scan())
    generate_pdf_report(results)

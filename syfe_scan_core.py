import asyncio
import aiohttp
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DOMAINS = ["api-uat-bugbounty.nonprod.syfe.com", "api.syfe.com"]
TOKENS = ["USER_TOKEN_1", "USER_TOKEN_2"]
ENDPOINTS = ["/api/v1/investments", "/api/v1/orders"]

async def test_endpoint(session, domain, endpoint, token):
    url = f"https://{domain}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        async with session.get(url, headers=headers) as resp:
            result = await resp.text()
            return domain, endpoint, resp.status, result[:200]
    except Exception as e:
        return domain, endpoint, "ERROR", str(e)

async def do_parallel_scan():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for domain in DOMAINS:
            for endpoint in ENDPOINTS:
                for token in TOKENS:
                    tasks.append(test_endpoint(session, domain, endpoint, token))
        results = await asyncio.gather(*tasks)
        return results

def generate_pdf_report(results, pdf_file):
    os.makedirs(os.path.dirname(pdf_file), exist_ok=True)
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

def run_scan(output_pdf_path):
    results = asyncio.run(do_parallel_scan())
    generate_pdf_report(results, output_pdf_path)

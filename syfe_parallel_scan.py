import sys
import os
from syfe_scan_core import run_scan

if len(sys.argv) > 1:
    output_pdf_path = sys.argv[1]
else:
    output_pdf_path = "syfe_parallel_scan_output/default_report.pdf"

os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

run_scan(output_pdf_path)
print(f"[+] PDF Report Generated: {output_pdf_path}")

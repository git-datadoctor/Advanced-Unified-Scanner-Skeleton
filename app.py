from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import datetime
import os

app = FastAPI(title="Syfe Parallel Scanner API")

# Ensure output directory exists
OUTPUT_DIR = "syfe_parallel_scan_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
async def home():
    return {"message": "Syfe Scanner API is running!"}

@app.post("/scan")
async def run_scan():
    try:
        # Unique PDF file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"Syfe_Parallel_BugBounty_Report_{timestamp}.pdf")
        
        # Run the scanner script (adjust if script accepts output path)
        subprocess.run(["python3", "syfe_parallel_scan.py", output_file], check=True)
        
        # Return PDF as download
        return FileResponse(output_file, media_type="application/pdf", filename=os.path.basename(output_file))
    
    except subprocess.CalledProcessError:
        return JSONResponse(status_code=500, content={"error": "Scanner execution failed."})

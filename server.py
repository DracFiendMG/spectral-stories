"""
server.py
Spectral Stories - FastAPI Web Service & AI Engine
Provides endpoints for the Digital Ofrenda, TabPFN Anomaly Detection, and Gothic Haunting Lore.
Compatible with Render web service deployment.
"""

import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from engine.tabpfn_analyzer import detector
from engine.story_engine import generate_ofrenda_memorial, generate_haunting_lore

app = FastAPI(
    title="Spectral Stories API",
    description="Digital Ofrenda & TabPFN Paranormal Anomaly Detection for Hacktoberfest 2026",
    version="1.0.0"
)

# Enable CORS for local testing and web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MemorialRequest(BaseModel):
    name: str
    relationship: str
    memory: str
    offerings: Optional[List[str]] = []

class AnomalyAnalyzeRequest(BaseModel):
    csv_content: str
    sensitivity: Optional[float] = 2.5

class LoreRequest(BaseModel):
    anomaly: Dict[str, Any]


@app.get("/api/health")
def health_check():
    """Health check endpoint for Render deployment."""
    return {
        "status": "online",
        "service": "Spectral Stories",
        "tabpfn_engine": detector.has_tabpfn,
        "mode": "Active"
    }


@app.post("/api/memorial")
def create_memorial(req: MemorialRequest):
    """Generates an evocative Día de los Muertos remembrance tribute."""
    if not req.name.strip():
        raise HTTPException(status_code=400, detail="Name is required.")
    
    result = generate_ofrenda_memorial(
        name=req.name.strip(),
        relationship=req.relationship.strip() or "Beloved Friend",
        memory=req.memory.strip() or "The quiet warmth of your presence and unyielding kindness.",
        offerings=req.offerings or ["Cempasúchil Marigolds", "Candlelight", "Pan de Muerto"]
    )
    return result


@app.post("/api/detect")
def analyze_telemetry(req: AnomalyAnalyzeRequest):
    """Analyzes CSV time-series telemetry using TabPFN tabular foundation network."""
    try:
        results = detector.analyze_csv_content(req.csv_content, sensitivity=req.sensitivity)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/detect-file")
async def analyze_telemetry_file(file: UploadFile = File(...), sensitivity: float = Form(2.5)):
    """Upload CSV file for TabPFN anomaly detection."""
    try:
        content = (await file.read()).decode("utf-8")
        results = detector.analyze_csv_content(content, sensitivity=sensitivity)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/sample-data/{dataset}")
def get_sample_dataset(dataset: str):
    """Returns sample datasets: 'smart_home' or 'server_rack'."""
    filename_map = {
        "smart_home": "data/smart_home_october.csv",
        "server_rack": "data/server_rack_telemetry.csv"
    }
    path = filename_map.get(dataset)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Dataset not found.")
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"dataset": dataset, "csv_content": content}


@app.post("/api/haunting-lore")
def create_haunting_lore(req: LoreRequest):
    """Generates gothic folklore from detected tabular anomalies."""
    result = generate_haunting_lore(req.anomaly)
    return result


# Serve static web frontend
if os.path.exists("index.html"):
    @app.get("/")
    def serve_index():
        return FileResponse("index.html")

    @app.get("/styles.css")
    def serve_css():
        return FileResponse("styles.css", media_type="text/css")

    @app.get("/app.js")
    def serve_js():
        return FileResponse("app.js", media_type="application/javascript")

# Mount static folders if they exist
if os.path.exists("assets"):
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")
if os.path.exists("data"):
    app.mount("/data", StaticFiles(directory="data"), name="data")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Spectral Stories server on http://localhost:{port}")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)

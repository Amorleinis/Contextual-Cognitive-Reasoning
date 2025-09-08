from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from core.context_engine import ContextEngine
from simulation.threat_simulator import ThreatSimulator
from multimodal.audio_analyzer import AudioAnalyzer
import shutil
import os

app = FastAPI(title="Contextual Reasoner API")

engine = ContextEngine()

class TextInput(BaseModel):
    text: str

@app.post("/analyze/text")
def analyze_text(data: TextInput):
    return engine.analyze_text(data.text)

@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = engine.analyze_image(temp_path)
    os.remove(temp_path)
    return result

@app.post("/analyze/audio")
async def analyze_audio(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    analyzer = AudioAnalyzer()
    result = analyzer.analyze_audio(temp_path)
    os.remove(temp_path)
    return {"transcription": result}

@app.post("/simulate/threats")
def simulate_threats():
    simulator = ThreatSimulator()
    simulator.simulate()
    return {"status": "Simulation completed"}
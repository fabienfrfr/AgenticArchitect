from fastapi import FastAPI
from apps.backend.agents.analyst.agent import AnalystAgent
from apps.backend.agents.architect.agent import ArchitectAgent
from apps.backend.agents.engineer.agent import EngineerAgent
from apps.backend.core.nemotron import NemotronInference

app = FastAPI()
analyst = AnalystAgent()
architect = ArchitectAgent()
engineer = EngineerAgent()
nemotron = NemotronInference()

@app.post("/analyze_cdc")
def analyze_cdc(cdc_text: str):
    return analyst.analyze(cdc_text)

@app.post("/generate_c4")
def generate_c4(requirements: dict):
    return {"diagram": architect.generate_c4_diagram(requirements)}

@app.post("/generate_adr")
def generate_adr(context: dict):
    return architect.generate_adr(context)

@app.post("/generate_code")
def generate_code(adr: dict, c4_diagram: dict):
    return engineer.generate_solid_code(adr, c4_diagram)

@app.post("/nemotron_inference")
def nemotron_inference(prompt: str):
    return {"response": nemotron.generate(prompt)}

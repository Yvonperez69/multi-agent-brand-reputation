from fastapi import FastAPI
from pydantic import BaseModel
from graph import compiled_graph

app = FastAPI()

class AnalyzeRequest(BaseModel):
    brand: str
    
@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    result = compiled_graph.invoke({"brand": request.brand})
    return {"result": result}
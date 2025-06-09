from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from pearls_model import PEARLSModel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PEARLS model
pearls_model = PEARLSModel()

class DebriefRequest(BaseModel):
    text: str

class DebriefResponse(BaseModel):
    response: str

@app.post("/debrief", response_model=DebriefResponse)
async def debrief(request: DebriefRequest):
    try:
        response = pearls_model.process_input(request.text)
        return DebriefResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
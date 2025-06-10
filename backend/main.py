from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from pearls_model import PEARLSModel
import logging

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize PEARLS model
pearls_model = PEARLSModel()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DebriefRequest(BaseModel):
    text: str

class DebriefResponse(BaseModel):
    response: str

@app.post("/debrief", response_model=DebriefResponse)
async def debrief(request: DebriefRequest):
    try:
        logger.info(f"Received debrief request: {request.text[:100]}...")  # Log first 100 chars
        response = pearls_model.process_input(request.text)
        logger.info("Successfully generated response")
        return DebriefResponse(response=response)
    except Exception as e:
        logger.error(f"Error in debrief endpoint: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"API error response: {e.response.text}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    logger.info("Health check endpoint called")
    return {
        "status": "ok",
        "service": "SimBox Debrief AI Agent",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
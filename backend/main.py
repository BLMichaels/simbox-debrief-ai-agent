import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pearls_model import PEARLSModel, PERPLEXITY_API_KEY
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate environment variables
if not PERPLEXITY_API_KEY:
    logger.error("PERPLEXITY_API_KEY environment variable is not set!")
    raise ValueError("PERPLEXITY_API_KEY environment variable is not set")

logger.info("Environment variables loaded successfully")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class DebriefRequest(BaseModel):
    text: str

class DebriefResponse(BaseModel):
    response: str

# Initialize PEARLS model
try:
    pearls_model = PEARLSModel()
    logger.info("PEARLS model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize PEARLS model: {e}")
    pearls_model = None

# Update environment variable validation and health check for OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "api_key_configured": bool(OPENAI_API_KEY)
    }

@app.post("/debrief")
async def debrief(request: DebriefRequest):
    try:
        logger.info(f"Received debrief request: {request.text[:100]}...")  # Log first 100 chars
        response = pearls_model.process_input(request.text)
        logger.info("Successfully generated response")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in debrief endpoint: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"API error response: {e.response.text}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
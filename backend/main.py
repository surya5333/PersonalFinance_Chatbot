import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import chatbot

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Personal Finance Chatbot API",
    description="API for Personal Finance Chatbot with Gemini and Granite integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chatbot.router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Personal Finance Chatbot API is running"}

if __name__ == "__main__":
    host = os.getenv("BACKEND_HOST", "127.0.0.1")
    port = int(os.getenv("BACKEND_PORT", 8000))
    
    print(f"Starting Personal Finance Chatbot API on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
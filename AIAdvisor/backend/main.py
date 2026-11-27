
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.eligibility_routes import router as eligibility_router

from routes.chat_routes import router as chat_router

# Create FastAPI application
app = FastAPI(
    title="AI Advisor & Smart Autofill",
    description="AI-powered government scheme guidance and application assistance",
    version="1.0.0"
)

# Allow communication with React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register API routers
app.include_router(chat_router)
app.include_router(eligibility_router)


# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Advisor!",
        "status": "Backend is running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI Advisor"
    }

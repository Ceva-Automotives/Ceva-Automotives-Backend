from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings

app = FastAPI(
    title="Ceva Automotives API",
    description="Backend API for Ceva Automotives - Sistema de Locação de Veículos",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from .carros.router import router as carros_router

app.include_router(carros_router)

@app.get('/')
async def hello_world():
    return {
        "status": 'online',
        "message": "Welcome to Ceva Automotives API",
        "version": "1.0.0"
    }

@app.get('/health')
async def health_check():
    return {
        "status": "healthy", 
        "message": "API is running",
        "environment": settings.environment
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)

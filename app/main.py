from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .admins.router import router as admins_router
from .avaliacoes.router import router as avaliacoes_router
from .carros.router import router as carros_router
from .clientes.router import router as clientes_router
from .config import settings
from .dashboards.router import router as dashboards_router
from .localizacoes.router import router as localizacoes_router
from .metricas.router import router as metricas_router
from .reservas.router import router as reservas_router

app = FastAPI(
    title="Ceva Automotives API",
    description="Backend API for Ceva Automotives - Sistema de Locação de Veículos",
    version="2.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(carros_router)
app.include_router(clientes_router)
app.include_router(admins_router)
app.include_router(localizacoes_router)
app.include_router(reservas_router)
app.include_router(avaliacoes_router)
app.include_router(dashboards_router)
app.include_router(metricas_router)

@app.get('/')
async def hello_world():
    return {
        "status": 'online',
        "message": "Welcome to Ceva Automotives API",
        "version": "2.0.0"
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

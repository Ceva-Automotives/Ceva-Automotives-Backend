from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    db_connect_url: str = "sqlite:///./ceva.db"
    
    # Variáveis originais do projeto (para compatibilidade)
    postgres_db: str = "ceva_db"
    postgres_user: str = "ceva_user" 
    postgres_password: str = "ceva_password"
    
    # API configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        extra = "allow"  # ← Permite variáveis extras

settings = Settings()

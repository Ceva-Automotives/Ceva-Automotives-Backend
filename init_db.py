#!/usr/bin/env python3
"""Script para inicializar o banco de dados"""

from src.database import engine, Base
from src.model.model import Carros

def init_database():
    """Cria todas as tabelas no banco de dados"""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_database()

#!/usr/bin/env python3
"""Script para inicializar o banco de dados"""

from sqlalchemy.schema import CreateTable

import app.model.model as models
from app.database import engine


def init_database():
    """Cria todas as tabelas no banco de dados"""
    print("Criando tabelas no banco de dados...")
    models.Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")
    print("Gerando modelo físico do banco em model_fisico.sql...")
    ddl_statements = []
    for table in models.Base.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(engine))
        ddl_statements.append(ddl + ";\n")
    with open("model_fisico.sql", "w") as f:
        f.writelines(ddl_statements)
    print("Modelo físico gerado com sucesso!")

if __name__ == "__main__":
    init_database()

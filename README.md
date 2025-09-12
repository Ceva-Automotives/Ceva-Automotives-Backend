# Ceva-Automotives-Backend

Backend API para Ceva Automotives desenvolvido com FastAPI e PostgreSQL.

## 🚀 Como executar com Docker

### Pré-requisitos
- Docker
- Docker Compose

### Desenvolvimento

1. Clone o repositório
2. Copie o arquivo de exemplo de variáveis de ambiente:
   ```bash
   cp env.example .env
   ```

3. Execute os serviços:
   ```bash
   docker-compose up -d
   ```

4. A API estará disponível em: http://localhost:8000
5. O banco PostgreSQL estará disponível em: localhost:5432

### Produção

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📁 Estrutura do Projeto

```
.
├── app/
│   ├── __init__.py
│   └── main.py              # Aplicação FastAPI principal
├── docker-compose.yml       # Configuração para desenvolvimento
├── docker-compose.prod.yml  # Configuração para produção
├── Dockerfile              # Imagem da aplicação
├── requirements.txt        # Dependências Python
├── init.sql               # Script de inicialização do banco
├── env.example            # Exemplo de variáveis de ambiente
└── .dockerignore          # Arquivos ignorados no build
```

## 🔧 Comandos Úteis

- **Ver logs**: `docker-compose logs -f`
- **Parar serviços**: `docker-compose down`
- **Rebuild**: `docker-compose up --build`
- **Acessar container**: `docker-compose exec api bash`
- **Acessar banco**: `docker-compose exec db psql -U ceva_user -d ceva_db`

## 🌐 Endpoints

- `GET /` - Página inicial
- `GET /health` - Health check
- `GET /docs` - Documentação interativa (Swagger)
- `GET /redoc` - Documentação alternativa (ReDoc)
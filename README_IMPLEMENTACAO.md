# Sistema de Aluguel de Carros - Implementação Completa

## Visão Geral

Este projeto implementa um sistema completo de aluguel de carros com FastAPI e PostgreSQL, baseado no diagrama de classes fornecido. Todas as entidades do diagrama foram implementadas seguindo os mesmos padrões e estrutura do CRUD de carros original.

## Estrutura do Projeto

```
app/
├── model/
│   └── model.py              # Todos os modelos SQLAlchemy
├── carros/                   # CRUD de Carros (atualizado)
│   ├── __init__.py
│   ├── repository.py
│   ├── router.py
│   └── schema.py
├── clientes/                 # CRUD de Clientes
│   ├── __init__.py
│   ├── repository.py
│   ├── router.py
│   └── schema.py
├── admins/                   # CRUD de Administradores
│   ├── __init__.py
│   ├── repository.py
│   ├── router.py
│   └── schema.py
├── localizacoes/            # CRUD de Localizações
│   ├── __init__.py
│   ├── repository.py
│   ├── router.py
│   └── schema.py
├── reservas/                # CRUD de Reservas
│   ├── __init__.py
│   ├── repository.py
│   ├── router.py
│   └── schema.py
├── avaliacoes/              # CRUD de Avaliações
│   ├── __init__.py
│   ├── repository.py
│   ├── router.py
│   └── schema.py
├── dashboards/              # CRUD de Dashboards
│   ├── __init__.py
│   ├── repository.py
│   ├── router.py
│   └── schema.py
├── metricas/                # CRUD de Métricas
│   ├── __init__.py
│   ├── repository.py
│   ├── router.py
│   └── schema.py
├── config.py
├── database.py
├── main.py
└── security.py
```

## Classes Implementadas

### 1. Usuario (Classe Base Abstrata)
- Classe base para Cliente e Admin
- Herança usando SQLAlchemy Joined Table Inheritance
- Atributos: id, nome, email, senha, telefone, dataCadastro, tipo

### 2. Cliente (Herda de Usuario)
- Atributos específicos: cnh, cpf
- Relacionamentos: reservas, avaliacoes
- Endpoints: CRUD completo + login + contagem

### 3. Admin (Herda de Usuario)
- Atributos específicos: cargo
- Relacionamento: dashboard
- Endpoints: CRUD completo + login + busca por cargo

### 4. Localizacao
- Atributos: id, nome, endereco
- Relacionamentos: carros, reservas_retirada, reservas_devolucao
- Endpoints: CRUD completo + busca por nome

### 5. Carros (Atualizado)
- Novos atributos: placa, categoria, status, localizacaoId
- Relacionamentos: localizacao, avaliacoes, reservas
- Mantém todos os endpoints originais

### 6. Reserva
- Atributos: id, dataRetirada, dataDevolucao, valorTotal, status
- Relacionamentos: cliente, carro, localizacaoRetirada, localizacaoDevolucao
- Endpoints: CRUD completo + confirmar/cancelar/concluir + buscas por cliente/carro/status
- Cálculo automático de valor total

### 7. Avaliacao
- Atributos: id, nota (1-5), comentario, data
- Relacionamentos: cliente, carro
- Endpoints: CRUD completo + média por carro + buscas por cliente/carro/nota

### 8. Dashboard
- Atributos: id, nome, adminId
- Relacionamento: admin, metricas
- Endpoints: CRUD completo + busca por admin

### 9. Metrica
- Atributos: id, nome, valor, tipo, dashboardId
- Relacionamento: dashboard
- Endpoints: CRUD completo + buscas por dashboard/tipo

## Relacionamentos Implementados

1. **Cliente 1 -- 0..* Reserva**: Um cliente pode ter várias reservas
2. **Reserva 1 -- 1 Carro**: Uma reserva aluga um carro
3. **Reserva 1 -- 1 Localizacao** (retirada e devolução): Duas localizações por reserva
4. **Carro 1 -- 0..* Avaliacao**: Um carro pode ter várias avaliações
5. **Cliente 1 -- 0..* Avaliacao**: Um cliente pode escrever várias avaliações
6. **Localizacao 1 -- 0..* Carro**: Uma localização pode ter vários carros
7. **Admin 1 -- 1 Dashboard**: Um admin tem um dashboard
8. **Dashboard 1 -- 1..* Metrica**: Um dashboard tem várias métricas

## Enums Implementados

```python
class StatusCarro(str, enum.Enum):
    DISPONIVEL = "Disponivel"
    ALUGADO = "Alugado"
    MANUTENCAO = "Manutencao"

class StatusReserva(str, enum.Enum):
    PENDENTE = "Pendente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    CONCLUIDA = "Concluida"
```

## Endpoints Principais

### Clientes
- `POST /clientes/` - Criar cliente
- `POST /clientes/login` - Login de cliente
- `GET /clientes/` - Listar todos
- `GET /clientes/{id}` - Buscar por ID
- `PUT /clientes/{id}` - Atualizar cliente
- `DELETE /clientes/{id}` - Deletar cliente
- `GET /clientes/count/` - Contar clientes

### Admins
- `POST /admins/` - Criar admin
- `POST /admins/login` - Login de admin
- `GET /admins/` - Listar todos
- `GET /admins/{id}` - Buscar por ID
- `PUT /admins/{id}` - Atualizar admin
- `DELETE /admins/{id}` - Deletar admin
- `GET /admins/cargo/{cargo}` - Buscar por cargo

### Localizações
- `POST /localizacoes/` - Criar localização
- `GET /localizacoes/` - Listar todas
- `GET /localizacoes/{id}` - Buscar por ID
- `PUT /localizacoes/{id}` - Atualizar localização
- `DELETE /localizacoes/{id}` - Deletar localização
- `GET /localizacoes/nome/{nome}` - Buscar por nome

### Carros (Atualizados)
- Mantém todos os endpoints originais
- Novos campos: placa, categoria, status, localizacaoId

### Reservas
- `POST /reservas/` - Criar reserva (calcula valor automaticamente)
- `GET /reservas/` - Listar todas
- `GET /reservas/{id}` - Buscar por ID
- `PUT /reservas/{id}` - Atualizar reserva
- `DELETE /reservas/{id}` - Deletar reserva
- `GET /reservas/cliente/{cliente_id}` - Buscar por cliente
- `GET /reservas/carro/{carro_id}` - Buscar por carro
- `GET /reservas/status/{status}` - Buscar por status
- `PATCH /reservas/{id}/confirmar` - Confirmar reserva
- `PATCH /reservas/{id}/cancelar` - Cancelar reserva
- `PATCH /reservas/{id}/concluir` - Concluir reserva

### Avaliações
- `POST /avaliacoes/` - Criar avaliação
- `GET /avaliacoes/` - Listar todas
- `GET /avaliacoes/{id}` - Buscar por ID
- `PUT /avaliacoes/{id}` - Atualizar avaliação
- `DELETE /avaliacoes/{id}` - Deletar avaliação
- `GET /avaliacoes/cliente/{cliente_id}` - Buscar por cliente
- `GET /avaliacoes/carro/{carro_id}` - Buscar por carro
- `GET /avaliacoes/carro/{carro_id}/media` - Calcular média de avaliações
- `GET /avaliacoes/nota/{nota}` - Buscar por nota

### Dashboards
- `POST /dashboards/` - Criar dashboard
- `GET /dashboards/` - Listar todos
- `GET /dashboards/{id}` - Buscar por ID
- `PUT /dashboards/{id}` - Atualizar dashboard
- `DELETE /dashboards/{id}` - Deletar dashboard
- `GET /dashboards/admin/{admin_id}` - Buscar por admin

### Métricas
- `POST /metricas/` - Criar métrica
- `GET /metricas/` - Listar todas
- `GET /metricas/{id}` - Buscar por ID
- `PUT /metricas/{id}` - Atualizar métrica
- `DELETE /metricas/{id}` - Deletar métrica
- `GET /metricas/dashboard/{dashboard_id}` - Buscar por dashboard
- `GET /metricas/tipo/{tipo}` - Buscar por tipo

## Funcionalidades Especiais

### Autenticação
- Senhas hasheadas com bcrypt
- Endpoints de login para clientes e admins
- Validação de credenciais

### Validações
- Email único para usuários
- CPF e CNH únicos para clientes
- Placa única para carros
- Um dashboard por admin
- Nota de avaliação entre 1 e 5
- Datas de reserva válidas

### Cálculos Automáticos
- Valor total da reserva baseado em dias e preço diário do carro
- Média de avaliações por carro

### Gerenciamento de Status
- Status de carros: Disponível, Alugado, Manutenção
- Status de reservas: Pendente, Confirmada, Cancelada, Concluída
- Transições de status com validações

## Padrões Seguidos

1. **Nomenclatura**: camelCase para atributos (precoDia, criadoEm, dataCadastro)
2. **Estrutura**: Cada entidade em sua própria pasta com repository, router e schema
3. **Repository**: Métodos estáticos para operações CRUD
4. **Schema**: BaseModel, Request, Response e Update separados
5. **Router**: APIRouter com prefix, tags e responses
6. **Timestamps**: criadoEm e atualizadoEm em todas as tabelas
7. **Documentação**: Docstrings em português em todas as funções

## Como Executar

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente no arquivo `.env`:
```
db_connect_url=postgresql://user:password@localhost/dbname
```

3. Criar as tabelas no banco:
```bash
python init_db.py
```

4. Executar a aplicação:
```bash
uvicorn app.main:app --reload
```

5. Acessar a documentação interativa:
```
http://localhost:8000/docs
```

## Dependências

- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- alembic==1.12.1
- python-dotenv==1.0.0
- pydantic==2.5.0
- pydantic-settings==2.1.0
- passlib[bcrypt]==1.7.4

## Notas Importantes

1. Todas as classes do diagrama foram implementadas
2. Todos os relacionamentos foram configurados corretamente
3. A herança de Usuario foi implementada usando Joined Table Inheritance
4. Senhas são sempre hasheadas antes de salvar no banco
5. Validações garantem integridade dos dados
6. Endpoints de contagem e busca foram adicionados onde apropriado
7. A estrutura segue exatamente o padrão do CRUD de carros original

## Autor

Implementação baseada no diagrama de classes fornecido e no CRUD de carros existente.

from datetime import datetime, timedelta
from app.database import SessionLocal
from app.model.model import Admin, Dashboard, Metrica, Localizacao, Carros, Cliente, Reserva, Avaliacao, StatusReserva
from app.security import get_password_hash

def seed():
    db = SessionLocal()
    try:
        if db.query(Localizacao).count() == 0:
            matriz = Localizacao(nome="Matriz", endereco="Av. Central, 1000")
            filial = Localizacao(nome="Filial Norte", endereco="Rua das Flores, 200")
            db.add_all([matriz, filial])
            db.commit()
            db.refresh(matriz)
            db.refresh(filial)
        else:
            matriz = db.query(Localizacao).first()
            filial = db.query(Localizacao).offset(1).first() or matriz

        if db.query(Admin).count() == 0:
            admin = Admin(
                nome="Admin Principal",
                email="admin@ceva.com",
                senha=get_password_hash("admin123"),
                telefone="61999990000",
                tipo="admin",
                cargo="Gerente"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        else:
            admin = db.query(Admin).first()

        if db.query(Dashboard).count() == 0:
            dashboard = Dashboard(nome="Operacional", adminId=admin.id)
            db.add(dashboard)
            db.commit()
            db.refresh(dashboard)
        else:
            dashboard = db.query(Dashboard).first()

        if db.query(Metrica).count() == 0:
            m1 = Metrica(nome="Reservas Hoje", valor="5", tipo="contador", dashboardId=dashboard.id)
            m2 = Metrica(nome="Carros Disponíveis", valor="12", tipo="contador", dashboardId=dashboard.id)
            db.add_all([m1, m2])
            db.commit()

        if db.query(Carros).count() == 0:
            c1 = Carros(
                placa="ABC1D23",
                marca="Toyota",
                modelo="Corolla",
                ano=2022,
                cor="Prata",
                precoDia=180.0,
                categoria="Sedan",
                descricao="Confortável e econômico",
                disponivel=True,
                destaque=True,
                localizacaoId=matriz.id
            )
            c2 = Carros(
                placa="EFG4H56",
                marca="Honda",
                modelo="Civic",
                ano=2021,
                cor="Preto",
                precoDia=170.0,
                categoria="Sedan",
                descricao="Ágil e moderno",
                disponivel=True,
                destaque=False,
                localizacaoId=filial.id
            )
            db.add_all([c1, c2])
            db.commit()
            db.refresh(c1)
            db.refresh(c2)
        else:
            c1 = db.query(Carros).first()
            c2 = db.query(Carros).offset(1).first() or c1

        if db.query(Cliente).count() == 0:
            cli1 = Cliente(
                nome="João da Silva",
                email="joao@example.com",
                senha=get_password_hash("cliente123"),
                telefone="61988887777",
                tipo="cliente",
                cnh="01234567890",
                cpf="123.456.789-00"
            )
            cli2 = Cliente(
                nome="Maria Oliveira",
                email="maria@example.com",
                senha=get_password_hash("cliente123"),
                telefone="61977776666",
                tipo="cliente",
                cnh="09876543210",
                cpf="987.654.321-00"
            )
            db.add_all([cli1, cli2])
            db.commit()
            db.refresh(cli1)
            db.refresh(cli2)
        else:
            cli1 = db.query(Cliente).first()
            cli2 = db.query(Cliente).offset(1).first() or cli1

        if db.query(Reserva).count() == 0:
            retirada = datetime.now()
            devolucao = retirada + timedelta(days=3)
            valor_total = (c1.precoDia or 0.0) * 3
            r1 = Reserva(
                dataRetirada=retirada,
                dataDevolucao=devolucao,
                valorTotal=valor_total,
                status=StatusReserva.CONFIRMADA,
                clienteId=cli1.id,
                carroId=c1.id,
                localizacaoRetiradaId=matriz.id,
                localizacaoDevolucaoId=filial.id
            )
            db.add(r1)
            db.commit()
            db.refresh(r1)

        if db.query(Avaliacao).count() == 0:
            a1 = Avaliacao(nota=5, comentario="Excelente carro!", clienteId=cli1.id, carroId=c1.id)
            a2 = Avaliacao(nota=4, comentario="Muito bom.", clienteId=cli2.id, carroId=c2.id)
            db.add_all([a1, a2])
            db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    seed()

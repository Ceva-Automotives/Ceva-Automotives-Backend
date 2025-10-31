from sqlalchemy.orm import Session
from ..model.model import Cliente
from ..security import get_password_hash, verify_password

class ClientesRepository:
    @staticmethod
    def find_all(database: Session) -> list[Cliente]:
        '''Função para fazer uma query de todos os clientes da DB'''
        return database.query(Cliente).all()

    @staticmethod
    def save(database: Session, cliente: Cliente) -> Cliente:
        '''Função para salvar um objeto cliente na DB'''
        if cliente.id:
            database.merge(cliente)
        else:
            database.add(cliente)
        database.commit()
        database.refresh(cliente)
        return cliente

    @staticmethod
    def find_by_id(database: Session, id: int) -> Cliente:
        '''Função para fazer uma query por ID de um objeto cliente na DB'''
        return database.query(Cliente).filter(Cliente.id == id).first()

    @staticmethod
    def exists_by_id(database: Session, id: int) -> bool:
        '''Função que verifica se o ID dado existe na DB'''
        return database.query(Cliente).filter(Cliente.id == id).first() is not None

    @staticmethod
    def delete_by_id(database: Session, id: int) -> None:
        '''Função para excluir um objeto cliente da DB dado o ID'''
        cliente = database.query(Cliente).filter(Cliente.id == id).first()
        if cliente is not None:
            database.delete(cliente)
            database.commit()

    @staticmethod
    def find_by_email(database: Session, email: str) -> Cliente:
        '''Função para fazer uma query por email de um cliente na DB'''
        return database.query(Cliente).filter(Cliente.email == email).first()

    @staticmethod
    def find_by_cpf(database: Session, cpf: str) -> Cliente:
        '''Função para fazer uma query por CPF de um cliente na DB'''
        return database.query(Cliente).filter(Cliente.cpf == cpf).first()

    @staticmethod
    def find_by_cnh(database: Session, cnh: str) -> Cliente:
        '''Função para fazer uma query por CNH de um cliente na DB'''
        return database.query(Cliente).filter(Cliente.cnh == cnh).first()

    @staticmethod
    def authenticate(database: Session, email: str, senha: str) -> Cliente:
        '''Função para autenticar um cliente'''
        cliente = ClientesRepository.find_by_email(database, email)
        if cliente and verify_password(senha, cliente.senha):
            return cliente
        return None

    @staticmethod
    def count_all(database: Session) -> int:
        '''Função para fazer uma query de contagem de todos os clientes da DB'''
        return database.query(Cliente).count()

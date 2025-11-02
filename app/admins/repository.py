from sqlalchemy.orm import Session
from ..model.model import Admin
from ..security import get_password_hash, verify_password

class AdminsRepository:
    @staticmethod
    def find_all(database: Session) -> list[Admin]:
        '''Função para fazer uma query de todos os admins da DB'''
        return database.query(Admin).all()

    @staticmethod
    def save(database: Session, admin: Admin) -> Admin:
        '''Função para salvar um objeto admin na DB'''
        if admin.id:
            database.merge(admin)
        else:
            database.add(admin)
        database.commit()
        database.refresh(admin)
        return admin

    @staticmethod
    def find_by_id(database: Session, id: int) -> Admin:
        '''Função para fazer uma query por ID de um objeto admin na DB'''
        return database.query(Admin).filter(Admin.id == id).first()

    @staticmethod
    def exists_by_id(database: Session, id: int) -> bool:
        '''Função que verifica se o ID dado existe na DB'''
        return database.query(Admin).filter(Admin.id == id).first() is not None

    @staticmethod
    def delete_by_id(database: Session, id: int) -> None:
        '''Função para excluir um objeto admin da DB dado o ID'''
        admin = database.query(Admin).filter(Admin.id == id).first()
        if admin is not None:
            database.delete(admin)
            database.commit()

    @staticmethod
    def find_by_email(database: Session, email: str) -> Admin:
        '''Função para fazer uma query por email de um admin na DB'''
        return database.query(Admin).filter(Admin.email == email).first()

    @staticmethod
    def authenticate(database: Session, email: str, senha: str) -> Admin:
        '''Função para autenticar um admin'''
        admin = AdminsRepository.find_by_email(database, email)
        if admin and verify_password(senha, admin.senha):
            return admin
        return None

    @staticmethod
    def count_all(database: Session) -> int:
        '''Função para fazer uma query de contagem de todos os admins da DB'''
        return database.query(Admin).count()

    @staticmethod
    def find_by_cargo(database: Session, cargo: str) -> list[Admin]:
        '''Função para fazer uma query por cargo de admins na DB'''
        return database.query(Admin).filter(Admin.cargo.ilike(f"%{cargo}%")).all()

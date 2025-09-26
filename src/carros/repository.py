from sqlalchemy.orm import Session
from ..model.model import Carros

class CarrosRepository:
    @staticmethod
    def find_all(database: Session) -> list[Carros]:
        '''Função para fazer uma query de todos os carros da DB'''
        return database.query(Carros).all()

    @staticmethod
    def save(database: Session, carros: Carros) -> Carros:
        '''Função para salvar um objeto carro na DB'''
        if carros.id:
            database.merge(carros)
        else:
            database.add(carros)
        database.commit()
        database.refresh(carros)
        return carros

    @staticmethod
    def find_by_id(database: Session, id: int) -> Carros:
        '''Função para fazer uma query por ID de um objeto carro na DB'''
        return database.query(Carros).filter(Carros.id == id).first()

    @staticmethod
    def exists_by_id(database: Session, id: int) -> bool:
        '''Função que verifica se o ID dado existe na DB'''
        return database.query(Carros).filter(Carros.id == id).first() is not None

    @staticmethod
    def delete_by_id(database: Session, id: int) -> None:
        '''Função para excluir um objeto carro da DB dado o ID'''
        carros = database.query(Carros).filter(Carros.id == id).first()
        if carros is not None:
            database.delete(carros)
            database.commit()

    @staticmethod
    def count_all(database: Session) -> int:
        '''Função para fazer uma query de contagem de todos os carros da DB'''
        return database.query(Carros).count()
        
    @staticmethod
    def count_disponivel(database: Session) -> int:
        '''Função para fazer uma query de contagem de carros disponíveis da DB'''
        return database.query(Carros).filter(Carros.disponivel == True).count()

    @staticmethod
    def count_destaque(database: Session) -> int:
        '''Função para fazer uma query de contagem de carros em destaque da DB'''
        return database.query(Carros).filter(Carros.destaque == True).count()

    @staticmethod
    def find_by_marca(database: Session, marca: str) -> list[Carros]:
        '''Função para fazer uma query por marca de carros na DB'''
        return database.query(Carros).filter(Carros.marca.ilike(f"%{marca}%")).all()

    @staticmethod
    def find_disponivel(database: Session) -> list[Carros]:
        '''Função para fazer uma query de todos os carros disponíveis da DB'''
        return database.query(Carros).filter(Carros.disponivel == True).all()

    @staticmethod
    def find_destaque(database: Session) -> list[Carros]:
        '''Função para fazer uma query de todos os carros em destaque da DB'''
        return database.query(Carros).filter(Carros.destaque == True).all()

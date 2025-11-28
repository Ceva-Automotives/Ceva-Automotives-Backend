from sqlalchemy.orm import Session

from ..model.model import Localizacao


class LocalizacoesRepository:
    @staticmethod
    def find_all(database: Session) -> list[Localizacao]:
        '''Função para fazer uma query de todas as localizações da DB'''
        return database.query(Localizacao).all()

    @staticmethod
    def save(database: Session, localizacao: Localizacao) -> Localizacao:
        '''Função para salvar um objeto localização na DB'''
        if localizacao.id:
            database.merge(localizacao)
        else:
            database.add(localizacao)
        database.commit()
        database.refresh(localizacao)
        return localizacao

    @staticmethod
    def find_by_id(database: Session, id: int) -> Localizacao:
        '''Função para fazer uma query por ID de um objeto localização na DB'''
        return database.query(Localizacao).filter(Localizacao.id == id).first()

    @staticmethod
    def exists_by_id(database: Session, id: int) -> bool:
        '''Função que verifica se o ID dado existe na DB'''
        return database.query(Localizacao).filter(Localizacao.id == id).first() is not None

    @staticmethod
    def delete_by_id(database: Session, id: int) -> None:
        '''Função para excluir um objeto localização da DB dado o ID'''
        localizacao = database.query(Localizacao).filter(Localizacao.id == id).first()
        if localizacao is not None:
            database.delete(localizacao)
            database.commit()

    @staticmethod
    def count_all(database: Session) -> int:
        '''Função para fazer uma query de contagem de todas as localizações da DB'''
        return database.query(Localizacao).count()

    @staticmethod
    def find_by_nome(database: Session, nome: str) -> list[Localizacao]:
        '''Função para fazer uma query por nome de localizações na DB'''
        return database.query(Localizacao).filter(Localizacao.nome.ilike(f"%{nome}%")).all()

from sqlalchemy.orm import Session
from ..model.model import Metrica

class MetricasRepository:
    @staticmethod
    def find_all(database: Session) -> list[Metrica]:
        '''Função para fazer uma query de todas as métricas da DB'''
        return database.query(Metrica).all()

    @staticmethod
    def save(database: Session, metrica: Metrica) -> Metrica:
        '''Função para salvar um objeto métrica na DB'''
        if metrica.id:
            database.merge(metrica)
        else:
            database.add(metrica)
        database.commit()
        database.refresh(metrica)
        return metrica

    @staticmethod
    def find_by_id(database: Session, id: int) -> Metrica:
        '''Função para fazer uma query por ID de um objeto métrica na DB'''
        return database.query(Metrica).filter(Metrica.id == id).first()

    @staticmethod
    def exists_by_id(database: Session, id: int) -> bool:
        '''Função que verifica se o ID dado existe na DB'''
        return database.query(Metrica).filter(Metrica.id == id).first() is not None

    @staticmethod
    def delete_by_id(database: Session, id: int) -> None:
        '''Função para excluir um objeto métrica da DB dado o ID'''
        metrica = database.query(Metrica).filter(Metrica.id == id).first()
        if metrica is not None:
            database.delete(metrica)
            database.commit()

    @staticmethod
    def count_all(database: Session) -> int:
        '''Função para fazer uma query de contagem de todas as métricas da DB'''
        return database.query(Metrica).count()

    @staticmethod
    def find_by_dashboard(database: Session, dashboard_id: int) -> list[Metrica]:
        '''Função para fazer uma query por dashboard de métricas na DB'''
        return database.query(Metrica).filter(Metrica.dashboardId == dashboard_id).all()

    @staticmethod
    def find_by_tipo(database: Session, tipo: str) -> list[Metrica]:
        '''Função para fazer uma query por tipo de métricas na DB'''
        return database.query(Metrica).filter(Metrica.tipo.ilike(f"%{tipo}%")).all()

    @staticmethod
    def count_by_dashboard(database: Session, dashboard_id: int) -> int:
        '''Função para fazer uma query de contagem de métricas por dashboard na DB'''
        return database.query(Metrica).filter(Metrica.dashboardId == dashboard_id).count()

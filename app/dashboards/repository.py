from sqlalchemy.orm import Session
from ..model.model import Dashboard

class DashboardsRepository:
    @staticmethod
    def find_all(database: Session) -> list[Dashboard]:
        '''Função para fazer uma query de todos os dashboards da DB'''
        return database.query(Dashboard).all()

    @staticmethod
    def save(database: Session, dashboard: Dashboard) -> Dashboard:
        '''Função para salvar um objeto dashboard na DB'''
        if dashboard.id:
            database.merge(dashboard)
        else:
            database.add(dashboard)
        database.commit()
        database.refresh(dashboard)
        return dashboard

    @staticmethod
    def find_by_id(database: Session, id: int) -> Dashboard:
        '''Função para fazer uma query por ID de um objeto dashboard na DB'''
        return database.query(Dashboard).filter(Dashboard.id == id).first()

    @staticmethod
    def exists_by_id(database: Session, id: int) -> bool:
        '''Função que verifica se o ID dado existe na DB'''
        return database.query(Dashboard).filter(Dashboard.id == id).first() is not None

    @staticmethod
    def delete_by_id(database: Session, id: int) -> None:
        '''Função para excluir um objeto dashboard da DB dado o ID'''
        dashboard = database.query(Dashboard).filter(Dashboard.id == id).first()
        if dashboard is not None:
            database.delete(dashboard)
            database.commit()

    @staticmethod
    def count_all(database: Session) -> int:
        '''Função para fazer uma query de contagem de todos os dashboards da DB'''
        return database.query(Dashboard).count()

    @staticmethod
    def find_by_admin(database: Session, admin_id: int) -> Dashboard:
        '''Função para fazer uma query por admin de dashboard na DB'''
        return database.query(Dashboard).filter(Dashboard.adminId == admin_id).first()

    @staticmethod
    def exists_by_admin(database: Session, admin_id: int) -> bool:
        '''Função que verifica se já existe um dashboard para o admin dado'''
        return database.query(Dashboard).filter(Dashboard.adminId == admin_id).first() is not None

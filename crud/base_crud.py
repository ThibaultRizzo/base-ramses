from models.base_model import BaseModel
from sqlalchemy import select

class BaseCrud:
    base_cls: BaseModel

    @classmethod
    def get_by_id(cls, session, entity_id: str):
        stmt = select(cls.base_cls).where(cls.base_cls.id==entity_id)
        return session.scalars(stmt).one_or_none()

    @classmethod
    def get_one(cls, session, criterion: tuple):
        stmt = select(cls.base_cls).where(*criterion)
        return session.scalars(stmt).one_or_none()

    @classmethod
    def get_all(cls, session, criterion: tuple):
        stmt = select(cls.base_cls).where(*criterion)
        return session.scalars(stmt).all()
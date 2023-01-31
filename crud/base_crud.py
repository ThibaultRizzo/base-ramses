from models.base_model import BaseModel
from sqlalchemy import select
from typing import TypeVar, Generic, List

T = TypeVar('T')

class BaseCrud(Generic[T]):
    base_cls: BaseModel

    @classmethod
    def get_by_id(cls, session, entity_id: str) -> T:
        stmt = select(cls.base_cls).where(cls.base_cls.id==entity_id)
        return session.execute(stmt).scalars().one_or_none()

    @classmethod
    def get_one(cls, session, criterion: tuple) -> T:
        stmt = select(cls.base_cls).where(criterion)
        return session.execute(stmt).scalar_one_or_none()

    @classmethod
    def get_all(cls, session, criterion: tuple = None) -> List[T]:
        criterion = criterion or ()
        stmt = select(cls.base_cls).where(*criterion)
        return session.scalars(stmt).all()

    @classmethod
    def create_one(cls, session, payload: dict) -> T:
        new_entity = cls.base_cls(**payload)
        session.add(new_entity)
        session.flush()
        return new_entity
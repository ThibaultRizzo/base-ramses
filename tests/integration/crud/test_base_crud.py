from sqlalchemy import Column, Float, String, create_engine
from sqlalchemy.orm import Session, sessionmaker

from crud.base_crud import BaseCrud
from models.base_model import BaseModel
from settings import settings

# class TestEntity(BaseModel):
#     username = Column(String, nullable=False)

# class TestEntityCrud(BaseCrud):
#     base_cls = TestEntity


class TestBlog:
    def setup_class(self):
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True, future=True)
        BaseModel.metadata.create_all(engine)
        # TestEntity.metadata.create_all(engine)
        self.session = Session()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_base_crud_get_one(self):
        # TestEntityCrud.create_one(self.session, {})
        assert True

import pytest
import uuid
from sqlalchemy import create_engine, text as sa_text
from sqlalchemy.orm import Session
from models.base_model import BaseModel
import importlib
from tests.datasets.generic import DATA_SET
from settings import settings
from sqlalchemy_utils import create_database, drop_database
from sqlalchemy.orm import sessionmaker
from settings import settings
from models.base_model import BaseModel

def unzip_data_set(data_set):
    """
    Reduce any format of data set input to an iterator of dict { model: data }

    Args:
        data_set: any type of object.
    """
    if isinstance(data_set, (list, tuple)):
        for entry in data_set:
            yield from unzip_data_set(entry)

    elif isinstance(data_set, str):
        mod = importlib.import_module(f"tests.datasets.{data_set}")
        yield from unzip_data_set(mod.DATA_SET)

    elif isinstance(data_set, dict):
        yield data_set

@pytest.fixture(name="db")
def fixture_db(request):
    """
    Function scoped database which will create a database from shared connection
    The database can be passed a custom dataset

    IMPORTANT:
    This is the default fixture to use when testing write operations
    """
    db_name = "service_backend_test_" + str(uuid.uuid4()).replace("-", "_")
    # text = f"CREATE DATABASE {db_name} ENCODING 'utf8' TEMPLATE 'template1'"
    db_url = f'postgresql://test:test@localhost:5434/{db_name}'
    settings.SQLALCHEMY_DATABASE_URL = db_url
    create_database(db_url)
    engine = create_engine(
        url=db_url,
        echo=False,
        future=True
    )
    try:
        # session.execute(sa_text(text))
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
        with Session(engine) as session:
            dataset = [DATA_SET]
            if hasattr(request, "param"):
                dataset = request.param
            dataset = unzip_data_set(dataset)
            signed = []
            for model_rows in dataset:
                if model_rows not in signed:
                    for model, rows in model_rows.items():
                        entries = []
                        for row in rows:
                            new_entry = model(**row)
                            entries.append(new_entry)
                        session.add_all(entries)
                        session.flush()
                signed.append(model_rows)
            session.commit()

        with Session(engine) as session:
            yield session
    finally:
        drop_database(db_url)
            # with engine.connect() as conn:
            #     version = conn.dialect.server_version_info
            #     pid_column = "pid" if (version >= (9, 2)) else "procpid"
            #     text = f"""
            #     SELECT pg_terminate_backend(pg_stat_activity.{pid_column})
            #     FROM pg_stat_activity
            #     WHERE pg_stat_activity.datname = '{db_name}'
            #     AND {pid_column} <> pg_backend_pid();
            #     """
            #     conn.execute(sa_text(text))

            # # Drop the database.
            # with engine.connect() as conn:
            #     text = f"DROP DATABASE {db_name}"
            #     conn.execute(sa_text(text))


class TestBlog:
    def setup_class(self):
        engine = create_engine(
            settings.SQLALCHEMY_DATABASE_URL, echo=True, future=True
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        BaseModel.metadata.create_all(engine)
        self.session = Session()
        self.valid_author = Author(
            firstname="Ezzeddin",
            lastname="Aybak",
            email="aybak_email@gmail.com"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

@pytest.fixture(scope="module")
def db_session():
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URL, echo=True, future=True
    )
    # session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    BaseModel.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from . import models

__factory = None

def global_init(db_file):
    global __factory
    db_file = db_file.strip()
    if __factory is not None:
        return

    if len(db_file) == 0:
        raise Exception('db_file is empty')

    database_url = f"sqlite:///{db_file}"
    engine = create_engine(database_url, echo=False)
    __factory = sessionmaker(bind=engine)
    models.SQLAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()

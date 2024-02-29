from sqlalchemy import Engine
from memento.sql.schemas.models import Base


def migrate(engine: Engine):
    Base.metadata.create_all(engine)
    print("Migration successful")

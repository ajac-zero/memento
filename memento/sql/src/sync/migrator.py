from memento.sql.src.sync.manager import Manager
from memento.sql.schemas.models import Base
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ALEMBIC_INI_PATH = os.path.join(DIR_PATH, "..", "alembic.ini")
MIGRATION_DIR_PATH = os.path.join(DIR_PATH, "..", "migrations")


class Migrator(Manager):
    def __init__(self, sessionmaker: sessionmaker):
        super().__init__(sessionmaker)

    def update_database(self, connection: str) -> None:
        if connection == "sqlite:///:memory:":
            self.sqlalchemy_update()
        else:
            self.alembic_update(connection)

    def alembic_update(self, connection: str):
        alembic_cfg = Config(ALEMBIC_INI_PATH)
        alembic_cfg.set_main_option("script_location", MIGRATION_DIR_PATH)
        alembic_cfg.set_main_option("sqlalchemy.url", connection)
        command.upgrade(alembic_cfg, "head")

    def sqlalchemy_update(self):
        with self.sessionmaker() as session:
            Base.metadata.create_all(session.get_bind())
        self.register_user()
        self.register_assistant()

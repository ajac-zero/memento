from memento.sql.asynchronous.schemas.models import Base
from memento.sql.asynchronous.src.manager import Manager
from sqlalchemy.ext.asyncio import async_sessionmaker
from alembic.config import Config
from alembic import command
import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ALEMBIC_INI_PATH = os.path.join(DIR_PATH, "..", "alembic.ini")
MIGRATION_DIR_PATH = os.path.join(DIR_PATH, "..", "migrations")


class Migrator(Manager):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__(sessionmaker)

    def update_database(self, connection: str) -> None:
        if connection == "sqlite:///:memory:":
            raise NotImplemented("Async SQL in-memory not yet implemented")
        else:
            self.alembic_update(connection)

    def alembic_update(self, connection: str):
        alembic_cfg = Config(ALEMBIC_INI_PATH)
        alembic_cfg.set_main_option("script_location", MIGRATION_DIR_PATH)
        alembic_cfg.set_main_option("sqlalchemy.url", connection)
        command.upgrade(alembic_cfg, "head")

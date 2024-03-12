from memento.sql.src.sync.repository import Repository
from memento.sql.schemas.models import Assistant, User, Conversation
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

@pytest.fixture
def sm():
    return sessionmaker(bind=create_engine("sqlite:///test.db"))

@pytest.fixture
def repo(sm):
    return Repository(sm)

def test_create_user(repo: Repository):
    user = User(name="Anibal")
    id = repo.create(User)
    assert isinstance(id, int)

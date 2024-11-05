import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from memento import crud, models

engine = create_engine("sqlite://")

models.Base.metadata.create_all(engine)


@pytest.fixture
def session():
    with Session(engine) as s:
        yield s


def test_create_conversation(session):
    c = crud.create_conversation(session, "Sarahbot")

    assert isinstance(c, models.Conversation)
    assert c.agent == "Sarahbot"


def test_get_conversation(session):
    c = crud.get_conversation(session, 1)

    assert isinstance(c, models.Conversation)
    assert c.agent == "Sarahbot"


def test_soft_delete_conversation(session):
    c = crud.soft_delete_conversation(session, 1)

    assert isinstance(c, models.Conversation)
    assert c.archived is True


def test_hard_delete_conversation(session):
    crud.hard_delete_conversation(session, 1)

    with pytest.raises(Exception):
        crud.get_conversation(session, 1)

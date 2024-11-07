import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from memento import crud, models

engine = create_engine("postgresql://myuser:mypassword@localhost:5432/mydatabase")

models.Base.metadata.create_all(engine)


@pytest.fixture(scope="module")
def state():
    return {}


@pytest.fixture
def session():
    with Session(engine) as s:
        yield s


def test_create_conversation(session, state):
    c = crud.create_conversation(session, "Sarahbot")

    assert isinstance(c, models.Conversation)
    assert c.agent == "Sarahbot"

    state["id"] = c.id


def test_get_conversation(session, state):
    c = crud.get_conversation(session, state["id"])

    assert isinstance(c, models.Conversation)
    assert c.agent == "Sarahbot"


def test_create_message(session, state):
    m = models.Message(state["id"], "user", "hello", None, None)

    session.add(m)
    session.commit()

    assert m.role == "user"
    assert m.content == "hello"
    assert m.uuid is None


def test_soft_delete_conversation(session, state):
    c = crud.soft_delete_conversation(session, state["id"])

    assert isinstance(c, models.Conversation)
    assert c.archived is True


def est_hard_delete_conversation(session, state):
    crud.hard_delete_conversation(session, state["id"])

    with pytest.raises(Exception):
        crud.get_conversation(session, state["id"])

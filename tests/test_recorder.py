import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from memento import crud, models, recorder

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


@pytest.fixture
def re(session):
    return recorder.Recorder.from_conversation(session, 1)


def test_add_message(re):
    x = len(re.conversation.messages)

    re.add_message(role="system", content="hello!")

    assert len(re.conversation.messages) == (x + 1)


def test_commit_messages(session, re):
    re.add_message(role="system", content="You're an awesome robot")
    re.add_message(role="user", content="hello!")
    message_ids = re.commit_new_messages(session)

    for n, id in enumerate(message_ids, start=1):
        assert id == n

import pytest

from memento.models import Base, Conversation, Message

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)


@pytest.fixture
def session():
    with Session(engine) as s:
        yield s


def test_create_conversation(session):
    conversation = Conversation(agent="Michalbot")

    session.add(conversation)
    session.commit()

    assert isinstance(conversation.id, int)
    assert conversation.id == 1
    assert conversation.agent == "Michalbot"


def test_add_system_message(session):
    system_message = Message(1, content="You are an awesome robot")

    session.add(system_message)
    session.commit()

    assert isinstance(system_message.id, int)
    assert system_message.id == 1
    assert system_message.content == "You are an awesome robot"
    assert system_message.role == "system"
    assert system_message.tools is None
    assert system_message.feedback is None


def test_add_user_message(session):
    user_message = Message(2, role="user", content="Hello!")

    session.add(user_message)
    session.commit()

    assert isinstance(user_message.id, int)
    assert user_message.id == 2
    assert user_message.content == "Hello!"
    assert user_message.role == "user"
    assert user_message.tools is None
    assert user_message.feedback is None


def test_add_assistant_message(session):
    assistant_message = Message(2, role="assistant", content="Beep boop")

    session.add(assistant_message)
    session.commit()

    assert isinstance(assistant_message.id, int)
    assert assistant_message.id == 3
    assert assistant_message.content == "Beep boop"
    assert assistant_message.role == "assistant"
    assert assistant_message.tools is None
    assert assistant_message.feedback is None

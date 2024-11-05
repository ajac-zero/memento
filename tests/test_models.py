from uuid import UUID

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from memento.models import Base, Conversation, Message

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
    assert isinstance(conversation.uuid, UUID)


def test_add_system_message(session):
    system_message = Message(
        1, role="system", content="You are an awesome robot", tools=None, feedback=None
    )

    session.add(system_message)
    session.commit()

    assert isinstance(system_message.id, int)
    assert system_message.id == 1
    assert system_message.content == "You are an awesome robot"
    assert system_message.role == "system"
    assert system_message.tools is None
    assert system_message.feedback is None
    assert isinstance(system_message.uuid, UUID)


def test_add_user_message(session):
    user_message = Message(1, role="user", content="Hello!", tools=None, feedback=None)

    session.add(user_message)
    session.commit()

    assert isinstance(user_message.id, int)
    assert user_message.id == 2
    assert user_message.content == "Hello!"
    assert user_message.role == "user"
    assert user_message.tools is None
    assert user_message.feedback is None
    assert isinstance(user_message.uuid, UUID)


def test_add_assistant_message(session):
    assistant_message = Message(
        1, role="assistant", content="Beep boop", tools=None, feedback=None
    )

    session.add(assistant_message)
    session.commit()

    assert isinstance(assistant_message.id, int)
    assert assistant_message.id == 3
    assert assistant_message.content == "Beep boop"
    assert assistant_message.role == "assistant"
    assert assistant_message.tools is None
    assert assistant_message.feedback is None
    assert isinstance(assistant_message.uuid, UUID)


def test_add_assistant_message_with_tool(session):
    assistant_message = Message(
        1, role="assistant", content=None, tools='{"tool_id": "1234"}', feedback=None
    )

    session.add(assistant_message)
    session.commit()

    assert isinstance(assistant_message.id, int)
    assert assistant_message.id == 4
    assert assistant_message.content is None
    assert assistant_message.role == "assistant"
    assert assistant_message.tools == '{"tool_id": "1234"}'
    assert assistant_message.feedback is None
    assert isinstance(assistant_message.uuid, UUID)


def test_conversation_message_relation(session):
    statement = select(Conversation).where(Conversation.id == 1)
    result = session.scalars(statement)
    conversation = result.one()

    assert isinstance(conversation.uuid, UUID)

    for message in conversation.messages:
        assert isinstance(message, Message)
        assert isinstance(message.uuid, UUID)


def test_message_conversation_relation(session):
    statement = select(Message)
    messages = session.scalars(statement)

    for message in messages:
        assert isinstance(message.conversation, Conversation)
        assert isinstance(message.conversation.uuid, UUID)

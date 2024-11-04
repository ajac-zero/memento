from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy import select
from memento.models import Conversation, Message, Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite://")

sm = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def async_session():
    async with sm() as s:
        yield s


@pytest.mark.asyncio
async def test_setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_create_conversation(async_session):
    conversation = Conversation(agent="Michalbot")

    async_session.add(conversation)
    await async_session.commit()

    assert isinstance(conversation.id, int)
    assert conversation.id == 1
    assert conversation.agent == "Michalbot"
    assert isinstance(conversation.uuid, UUID)


@pytest.mark.asyncio
async def test_add_system_message(async_session):
    system_message = Message(
        1, role="system", content="You are an awesome robot", tools=None, feedback=None
    )

    async_session.add(system_message)
    await async_session.commit()

    assert isinstance(system_message.id, int)
    assert system_message.id == 1
    assert system_message.content == "You are an awesome robot"
    assert system_message.role == "system"
    assert system_message.tools is None
    assert system_message.feedback is None
    assert isinstance(system_message.uuid, UUID)


@pytest.mark.asyncio
async def test_add_user_message(async_session):
    user_message = Message(1, role="user", content="Hello!", tools=None, feedback=None)

    async_session.add(user_message)
    await async_session.commit()

    assert isinstance(user_message.id, int)
    assert user_message.id == 2
    assert user_message.content == "Hello!"
    assert user_message.role == "user"
    assert user_message.tools is None
    assert user_message.feedback is None
    assert isinstance(user_message.uuid, UUID)


@pytest.mark.asyncio
async def test_add_assistant_message(async_session):
    assistant_message = Message(
        1, role="assistant", content="Beep boop", tools=None, feedback=None
    )

    async_session.add(assistant_message)
    await async_session.commit()

    assert isinstance(assistant_message.id, int)
    assert assistant_message.id == 3
    assert assistant_message.content == "Beep boop"
    assert assistant_message.role == "assistant"
    assert assistant_message.tools is None
    assert assistant_message.feedback is None
    assert isinstance(assistant_message.uuid, UUID)


@pytest.mark.asyncio
async def test_add_assistant_message_with_tool(async_session):
    assistant_message = Message(
        1, role="assistant", content=None, tools='{"tool_id": "1234"}', feedback=None
    )

    async_session.add(assistant_message)
    await async_session.commit()

    assert isinstance(assistant_message.id, int)
    assert assistant_message.id == 4
    assert assistant_message.content is None
    assert assistant_message.role == "assistant"
    assert assistant_message.tools == '{"tool_id": "1234"}'
    assert assistant_message.feedback is None
    assert isinstance(assistant_message.uuid, UUID)


@pytest.mark.asyncio
async def test_conversation_message_relation(async_session):
    statement = select(Conversation).where(Conversation.id == 1)
    result = await async_session.scalars(statement)
    conversation = result.one()

    assert isinstance(conversation.uuid, UUID)

    for message in await conversation.awaitable_attrs.messages:
        assert isinstance(message, Message)
        assert isinstance(message.uuid, UUID)


@pytest.mark.asyncio
async def test_message_conversation_relation(async_session):
    statement = select(Message)
    messages = await async_session.scalars(statement)

    for message in messages:
        c = await message.awaitable_attrs.conversation
        assert isinstance(c, Conversation)
        assert isinstance(c.uuid, UUID)

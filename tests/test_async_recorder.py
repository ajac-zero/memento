import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from memento import models, crud, recorder

engine = create_async_engine("sqlite+aiosqlite://")

sm = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def async_session():
    async with sm() as s:
        yield s


@pytest.mark.asyncio
async def test_setup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@pytest.mark.asyncio
async def test_create_conversation(async_session):
    c = await crud.create_conversation_async(async_session, "Sarahbot")

    assert isinstance(c, models.Conversation)
    assert c.agent == "Sarahbot"


@pytest_asyncio.fixture
async def re(async_session):
    return await recorder.Recoder.from_conversation_async(async_session, 1)


@pytest.mark.asyncio
async def test_add_message(re):
    x = len(re.messages)
    y = len(re.new_messages)

    re.add_message(role="system", content="hello!")

    assert len(re.messages) == (x + 1)
    assert len(re.new_messages) == (y + 1)


@pytest.mark.asyncio
async def test_commit_messages(async_session, re):
    re.add_message(role="system", content="You're an awesome robot")
    re.add_message(role="user", content="hello!")
    message_ids = await re.commit_new_messages_async(async_session)

    for n, id in enumerate(message_ids, start=1):
        assert id == n

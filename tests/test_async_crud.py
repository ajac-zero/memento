import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from memento import crud, models

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


@pytest.mark.asyncio
async def test_get_conversation(async_session):
    c = await crud.get_conversation_async(async_session, 1)

    assert isinstance(c, models.Conversation)
    assert c.agent == "Sarahbot"


@pytest.mark.asyncio
async def test_soft_delete_conversation(async_session):
    c = await crud.soft_delete_conversation_async(async_session, 1)

    assert isinstance(c, models.Conversation)
    assert c.archived is True


@pytest.mark.asyncio
async def test_hard_delete_conversation(async_session):
    await crud.hard_delete_conversation_async(async_session, 1)

    with pytest.raises(Exception):
        await crud.get_conversation_async(async_session, 1)

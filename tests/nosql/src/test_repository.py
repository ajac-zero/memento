from memento.nosql.schemas.models import Assistant, Conversation
from memento.nosql.src.repository import Repository
import pytest_asyncio
import pytest


@pytest_asyncio.fixture
async def repo():
    return Repository.create("mongodb://localhost:27017")


@pytest.mark.asyncio
async def test_noqsl_repository(repo: Repository):
    assert isinstance(repo, Repository)


@pytest.mark.asyncio
async def test_read_assistant(repo: Repository):
    await repo.on()
    assistant = await repo.read(Assistant, name="assistant")
    assert isinstance(assistant, Assistant)

@pytest.mark.asyncio
async def test_read_all_assistants(repo: Repository):
    await repo.on()
    assistant = await repo.read(Assistant, name="assistant", all=True)
    assert isinstance(assistant, list)

@pytest.mark.asyncio
async def test_read_conversation(repo: Repository):
    await repo.on()
    conversation = await repo.read(Conversation, idx="conversation")
    assert conversation is None

@pytest.mark.asyncio
async def test_read_all_conversations(repo: Repository):
    await repo.on()
    conversation = await repo.read(Conversation, idx="conversation", all=True)
    assert conversation is None

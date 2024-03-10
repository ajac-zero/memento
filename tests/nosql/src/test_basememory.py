from memento.nosql.src.basememory import AsyncNoSQLMemory
from openai import AsyncAzureOpenAI
import pytest_asyncio
import pytest

@pytest_asyncio.fixture
async def mem():
    return AsyncNoSQLMemory.create("mongodb://localhost:27017")

@pytest_asyncio.fixture
async def ai():
    return AsyncAzureOpenAI()

@pytest.mark.asyncio
async def test_async_nosqlmemory(mem: AsyncNoSQLMemory):
    assert isinstance(mem, AsyncNoSQLMemory)

@pytest.mark.asyncio
async def test_async_azure_client(ai: AsyncAzureOpenAI):
    assert isinstance(ai, AsyncAzureOpenAI)

from memento.nosql.asynchronous.src.basememory import AsyncNoSQLMemory
from litellm import acompletion, ModelResponse
from openai.types.chat import ChatCompletion
from openai import AsyncAzureOpenAI
from typing import AsyncGenerator
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

@pytest.mark.asyncio
async def test_async_response(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    gen = memento(ai.chat.completions.create)
    response = await gen(message="Hello", model="gpt4-2")

    assert isinstance(response, ChatCompletion)

@pytest.mark.asyncio
async def test_async_response_decorator(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    @memento
    async def gen(*args, **kwargs):
        return await ai.chat.completions.create(*args, **kwargs)

    response = await gen(message="Hi", model="gpt4-2")

    assert isinstance(response, ChatCompletion)

@pytest.mark.asyncio
async def test_async_stream_response(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    gen = memento(ai.chat.completions.create, stream=True)
    response = gen(message="Hello", model="gpt4-2", stream=True)

    assert isinstance(response, AsyncGenerator)

@pytest.mark.asyncio
async def test_async_stream_response_decorator(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    @memento(stream=True)
    async def gen(*args, stream=True, **kwargs):
        return await ai.chat.completions.create(*args, **kwargs, stream=stream)

    response = gen(message="Hi", model="gpt4-2")

    assert isinstance(response, AsyncGenerator)

@pytest.mark.asyncio
async def test_async_response_func(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    gen = memento(acompletion)
    response = await gen(message="Hello", model="azure/gpt4-2")

    assert isinstance(response, ModelResponse)

@pytest.mark.asyncio
async def test_async_response_decorator_func(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    @memento
    async def gen(*args, **kwargs):
        return await acompletion(*args, **kwargs)

    response = await gen(message="Hi", model="azure/gpt4-2")

    assert isinstance(response, ModelResponse)

@pytest.mark.asyncio
async def test_async_stream_response_func(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    gen = memento(acompletion, stream=True)
    response = gen(message="Hello", model="azure/gpt4-2", stream=True)

    assert isinstance(response, AsyncGenerator)

@pytest.mark.asyncio
async def test_async_stream_response_decorator_func(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    @memento(stream=True)
    async def gen(*args, stream=True, **kwargs):
        return await acompletion(*args, **kwargs, stream=stream)

    response = gen(message="Hi", model="azure/gpt4-2")

    assert isinstance(response, AsyncGenerator)

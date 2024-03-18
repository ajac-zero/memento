from memento.nosql.synchronous.src.basememory import NoSQLMemory
from litellm import completion, ModelResponse
from openai.types.chat import ChatCompletion
from openai import AzureOpenAI
from typing import Generator
import pytest

@pytest.fixture
def mem():
    return NoSQLMemory.create("mongodb://localhost:27017")

@pytest.fixture
def ai():
    return AzureOpenAI()

def test_nosqlmemory(mem: NoSQLMemory):
    assert isinstance(mem, NoSQLMemory)

def testc_azure_client(ai: AzureOpenAI):
    assert isinstance(ai, AzureOpenAI)

def test_response(ai: AzureOpenAI):
    memento = NoSQLMemory.create("mongodb://localhost:27017")
    memento.on()

    gen = memento(ai.chat.completions.create)
    response = gen(message="Hello", model="gpt4-2")

    assert isinstance(response, ChatCompletion)

def test_response_decorator(ai: AzureOpenAI):
    memento = NoSQLMemory.create("mongodb://localhost:27017")
    memento.on()

    @memento
    def gen(*args, **kwargs):
        return ai.chat.completions.create(*args, **kwargs)

    response = gen(message="Hi", model="gpt4-2")

    assert isinstance(response, ChatCompletion)

def test_stream_response(ai: AzureOpenAI):
    memento = NoSQLMemory.create("mongodb://localhost:27017")
    memento.on()

    gen = memento(ai.chat.completions.create, stream=True)
    response = gen(message="Hello", model="gpt4-2", stream=True)

    assert isinstance(response, Generator)

def test_stream_response_decorator(ai: AzureOpenAI):
    memento = NoSQLMemory.create("mongodb://localhost:27017")
    memento.on()

    @memento(stream=True)
    async def gen(*args, stream=True, **kwargs):
        return ai.chat.completions.create(*args, **kwargs, stream=stream)

    response = gen(message="Hi", model="gpt4-2")

    assert isinstance(response, Generator)

### LiteLLM

def test_response_func():
    memento = NoSQLMemory.create("mongodb://localhost:27017")
    memento.on()

    gen = memento(completion)
    response = gen(message="Hello", model="azure/gpt4-2")

    assert isinstance(response, ModelResponse)

def test_response_decorator_func():
    memento = NoSQLMemory.create("mongodb://localhost:27017")
    memento.on()

    @memento
    def gen(*args, **kwargs):
        return completion(*args, **kwargs)

    response = gen(message="Hi", model="azure/gpt4-2")

    assert isinstance(response, ModelResponse)

def test_stream_response_func():
    memento = NoSQLMemory.create("mongodb://localhost:27017")
    memento.on()

    gen = memento(completion, stream=True)
    response = gen(message="Hello", model="azure/gpt4-2", stream=True)

    assert isinstance(response, Generator)

def test_stream_response_decorator_func():
    memento = NoSQLMemory.create("mongodb://localhost:27017")
    memento.on()

    @memento(stream=True)
    async def gen(*args, stream=True, **kwargs):
        return completion(*args, **kwargs, stream=stream)

    response = gen(message="Hi", model="azure/gpt4-2")

    assert isinstance(response, Generator)

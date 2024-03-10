from memento.nosql.src.manager import Manager
import pytest_asyncio
import pytest


@pytest_asyncio.fixture
async def man():
    return Manager.create("mongodb://localhost:27017")


@pytest.mark.asyncio
async def test_noqsl_manager(man: Manager):
    assert isinstance(man, Manager)


@pytest.mark.asyncio
async def test_noqsl_register_assistant(man: Manager):
    await man.on()
    id = await man.register_assistant(
        name="Jon Snow", system="You are the watcher in the wall..."
    )
    assert isinstance(id, str)

@pytest.mark.asyncio
async def test_noqsl_register_conversation(man: Manager):
    await man.on()
    id = await man.register_conversation(user="Daenerys", assistant="Jon Snow")
    assert isinstance(id, str)

@pytest.mark.asyncio
async def test_noqsl_delete_assistant(man: Manager):
    await man.on()
    id = await man.delete_assistant(name="Jon Snow")
    assert isinstance(id, str)

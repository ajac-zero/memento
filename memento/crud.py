from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session

from memento.models import Conversation, Message

## Conversation

### Sync


def create_conversation(session: Session, agent: str):
    conversation = Conversation(agent)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def get_conversation(session: Session, id: int | UUID):
    if isinstance(id, int):
        statement = select(Conversation).where(Conversation.id == id)
    elif isinstance(id, UUID):
        statement = select(Conversation).where(Conversation.uuid == id)
    result = session.scalars(statement)
    return result.one()


def soft_delete_conversation(session: Session, id: int | UUID):
    conversation = get_conversation(session, id)
    conversation.archived = True
    for message in conversation.messages:
        message.archived = True
    session.commit()
    return conversation


def hard_delete_conversation(session: Session, id: int | UUID):
    conversation = get_conversation(session, id)
    session.delete(conversation)
    session.commit()
    return conversation


### Async


async def create_conversation_async(session: AsyncSession, agent: str):
    conversation = Conversation(agent)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def get_conversation_async(session: AsyncSession, id: int | UUID):
    if isinstance(id, int):
        statement = select(Conversation).where(Conversation.id == id)
    elif isinstance(id, UUID):
        statement = select(Conversation).where(Conversation.uuid == id)
    result = await session.scalars(statement)
    return result.one()


async def soft_delete_conversation_async(session: AsyncSession, id: int | UUID):
    conversation = await get_conversation_async(session, id)
    conversation.archived = True
    for message in await conversation.awaitable_attrs.messages:
        message.archived = True
    await session.commit()
    return conversation


async def hard_delete_conversation_async(session: AsyncSession, id: int | UUID):
    conversation = await get_conversation_async(session, id)
    await session.delete(conversation)
    await session.commit()
    return conversation


# Message

## Sync


def get_message(session: Session, id: int | UUID):
    if isinstance(id, int):
        statement = select(Message).where(Message.id == id)
    elif isinstance(id, UUID):
        statement = select(Message).where(Message.uuid == id)
    result = session.scalars(statement)
    return result.one()


def update_message_feedback(session: Session, id: int | UUID, feedback: bool | None):
    message = get_message(session, id)
    message.feedback = feedback
    session.commit()
    session.refresh(message)
    return message


def soft_delete_message(session: Session, id: int | UUID):
    message = get_message(session, id)
    message.archived = True
    session.commit()
    session.refresh(message)
    return message


def hard_delete_message(session: Session, id: int | UUID):
    message = get_message(session, id)
    session.delete(message)
    return message


## Async


async def get_message_async(session: AsyncSession, id: int | UUID):
    if isinstance(id, int):
        statement = select(Message).where(Message.id == id)
    elif isinstance(id, UUID):
        statement = select(Message).where(Message.uuid == id)
    result = await session.scalars(statement)
    return result.one()


async def update_message_feedback_async(
    session: AsyncSession, id: int | UUID, feedback: bool | None
):
    message = await get_message_async(session, id)
    message.feedback = feedback
    await session.commit()


async def soft_delete_message_async(session: AsyncSession, id: int | UUID):
    message = await get_message_async(session, id)
    message.archived = True
    await session.commit()
    await session.refresh(message)
    return message


async def hard_delete_message_async(session: AsyncSession, id: int | UUID):
    message = await get_message_async(session, id)
    await session.delete(message)
    return message

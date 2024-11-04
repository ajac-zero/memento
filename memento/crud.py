from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio.session import AsyncSession

from memento.models import Conversation, Message


def get_conversation(session: Session, id: int):
    statement = select(Conversation).where(Conversation.id == id)
    result = session.scalars(statement)
    return result.one()


async def get_conversation_async(session: AsyncSession, id: int):
    statement = select(Conversation).where(Conversation.id == id)
    result = await session.scalars(statement)
    return result.one()


def get_conversation_by_uuid(session: Session, uuid: UUID):
    statement = select(Conversation).where(Conversation.uuid == uuid)
    result = session.scalars(statement)
    return result.one()


async def get_conversation_by_uuid_async(session: AsyncSession, uuid: UUID):
    statement = select(Conversation).where(Conversation.uuid == uuid)
    result = await session.scalars(statement)
    return result.one()


def get_message(session: Session, id: int):
    statement = select(Message).where(Message.id == id)
    result = session.scalars(statement)
    return result.one()


def get_message_by_uuid(session: Session, uuid: UUID):
    statement = select(Message).where(Message.uuid == uuid)
    result = session.scalars(statement)
    return result.one()


async def get_message_async(session: AsyncSession, id: int):
    statement = select(Message).where(Message.id == id)
    result = await session.scalars(statement)
    return result.one()


async def get_message_by_uuid_async(session: AsyncSession, uuid: UUID):
    statement = select(Message).where(Message.uuid == uuid)
    result = await session.scalars(statement)
    return result.one()

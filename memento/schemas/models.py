from sqlalchemy.orm import declarative_base, relationship, mapped_column as column
from sqlalchemy import Integer, String, Text, ForeignKey
from typing import Optional


Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = column(Integer, primary_key=True)
    name = column(String(30), nullable=False, unique=True)
    conversations = relationship("Conversation", cascade="all, delete")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"


class Assistant(Base):
    __tablename__ = "Assistants"

    id = column(Integer, primary_key=True)
    name = column(String(20), nullable=False, unique=True)
    system = column(Text, nullable=False)
    model = column(String(20))
    tokens = column(Integer)
    conversation = relationship("Conversation", cascade="all, delete")

    def __repr__(self) -> str:
        return f"Assistant(id={self.id}, name={self.name}, system_prompt={self.system}, model={self.model}, max_tokens={self.tokens})"


class Conversation(Base):
    __tablename__ = "Conversations"

    id = column(Integer, primary_key=True)
    name = column(Text)
    user = column(ForeignKey("Users.id"), nullable=False)
    assistant = column(ForeignKey("Assistants.id"), nullable=False)
    messages = relationship("Message", cascade="all,delete", lazy="joined")

    def __repr__(self) -> str:
        return f"Conversation(id={self.id}, name={self.name}, assistant={self.assistant}, user={self.user})"


class Message(Base):
    __tablename__ = "Messages"

    id = column(Integer, primary_key=True)
    conversation = column(ForeignKey("Conversations.id"), nullable=False)

    role = column(String(9), nullable=False)
    content = column(Text, nullable=False)
    prompt = column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"""Message(id={self.id}, conversation={self.conversation}, role="{self.role}", content="{self.content}")"""

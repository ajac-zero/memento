from memento.sql.asynchronous.schemas.models import Assistant, Conversation, Message, User
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import overload, Literal, Sequence
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

class Repository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def create(self, instance: User | Assistant | Conversation | Message) -> int:
        async with self.sessionmaker() as session:
            if isinstance(instance, User) or isinstance(instance, Assistant):
                stmt = select(instance.__class__).filter_by(name=instance.name)
                existing_model = await session.scalars(stmt)
                if existing_model.first() is None:
                    session.add(instance)
                    await session.commit()
                    return await instance.awaitable_attrs.id
                else:
                    raise ValueError(
                        f"{instance.__class__.__name__} already registered"
                    )
            else:
                session.add(instance)
                await session.commit()
                return await instance.awaitable_attrs.id

    async def delete(self, model: type[User] | type[Assistant] | type[Conversation], **kwargs) -> None:
        async with self.sessionmaker() as session:
            try:
                stmt = select(model).filter_by(**kwargs)
                existing_model = (await session.scalars(stmt)).unique().first()
                await session.delete(existing_model)
                await session.commit()
            except NoResultFound:
                raise ValueError(
                    f"{model.__name__} cannot be deleted because it does not exist."
                )

    @overload
    async def read(self, model: type[User], all: bool = False, **kwargs) -> User | None: ...

    @overload
    async def read(self, model: type[Conversation], all: Literal[False] = False, **kwargs) -> Conversation | None: ...

    @overload
    async def read(self, model: type[Conversation], all: Literal[True], **kwargs) -> list[Conversation] | None: ...

    @overload
    async def read(self, model: type[Conversation], all: bool = False, **kwargs): ...

    @overload
    async def read(self, model: type[Assistant], all: bool = False, **kwargs) -> Assistant | None: ...

    async def read(
        self,
        model: type[User] | type[Assistant] | type[Conversation],
        all: bool = False,
        **kwargs,
    ) -> User | Assistant | Conversation | Sequence[User | Assistant | Conversation] | None:
        async with self.sessionmaker() as session:
            stmt = select(model).filter_by(**kwargs)
            query = (await session.scalars(stmt)).unique()
            return query.all() if all else query.first()

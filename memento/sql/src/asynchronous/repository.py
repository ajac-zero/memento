from memento.sql.schemas.models import Assistant, Conversation, Message, User
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
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
                    return instance.id
                else:
                    raise ValueError(
                        f"{instance.__class__.__name__} already registered"
                    )
            else:
                session.add(instance)
                await session.commit()
                return instance.id

    async def delete(self, model: type[User] | type[Assistant] | type[Conversation], **kwargs) -> None:
        async with self.sessionmaker() as session:
            try:
                stmt = select(model).filter_by(**kwargs)
                existing_model = await session.scalars(stmt)
                await session.delete(existing_model.first())
                await session.commit()
            except NoResultFound:
                raise ValueError(
                    f"{model.__name__} cannot be deleted because it does not exist."
                )

    async def read(
        self,
        model: User | Assistant | Conversation,
        all: bool = False,
        **kwargs,
    ) -> User | Assistant | Conversation | None:
        async with self.sessionmaker() as session:
            stmt = select(model).filter_by(**kwargs)
            query = await session.scalars(stmt)
            return query.all() if all else query.first() #type: ignore

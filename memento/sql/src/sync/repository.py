from memento.sql.schemas.models import Assistant, Conversation, Message, User
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker


class Repository:
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    def create(self, instance: User | Assistant | Conversation | Message) -> int:
        with self.sessionmaker() as session:
            if isinstance(instance, User) or isinstance(instance, Assistant):
                existing_model = (
                    session.query(instance.__class__)
                    .filter_by(name=instance.name)
                    .first()
                )
                if existing_model is None:
                    session.add(instance)
                    session.commit()
                    return instance.id
                else:
                    raise ValueError(
                        f"{instance.__class__.__name__} already registered"
                    )
            else:
                session.add(instance)
                session.commit()
                return instance.id

    def delete(self, model: User | Assistant | Conversation, **kwargs) -> None:
        with self.sessionmaker() as session:
            try:
                existing_model = session.query(model).filter_by(**kwargs).one()
                session.delete(existing_model)
                session.commit()
            except NoResultFound:
                raise ValueError(
                    f"{model.__class__.__name__} cannot be deleted because it does not exist."
                )

    def read(
        self,
        model: User | Assistant | Conversation,
        all: bool = False,
        **kwargs,
    ) -> User | Assistant | Conversation | None:
        with self.sessionmaker() as session:
            query = session.query(model).filter_by(**kwargs)
            return query.all() if all else query.first()

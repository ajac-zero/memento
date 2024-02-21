from memento.schemas.models import Assistant, Conversation, Message, User
from typing import Union, Optional, List
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker


class Repository:
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    def create(self, instance: Union[User, Assistant, Conversation, Message]) -> int:
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

    def delete(self, model: Union[User, Assistant, Conversation], **kwargs) -> bool:
        with self.sessionmaker() as session:
            try:
                existing_model = session.query(model).filter_by(**kwargs).one()
                session.delete(existing_model)
                session.commit()
                return True
            except NoResultFound:
                raise ValueError(
                    f"{model.__class__.__name__} cannot be deleted because it does not exist."
                )

    def read(
        self,
        model: Union[User, Assistant, Conversation],
        all: bool = False,
        **kwargs,
    ) -> Optional[Union[User, Assistant, Conversation]]:
        with self.sessionmaker() as session:
            query = session.query(model).filter_by(**kwargs)
            return query.all() if all else query.first()

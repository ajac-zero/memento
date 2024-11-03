if __name__ == "__main__":
    from memento.models import Base, Conversation, Message

    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine("sqlite:///test.db")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        conversation = Conversation(agent="Michalbot")

        session.add(conversation)
        session.commit()

        if conversation.id:
            m1 = Message(
                conversation_id=conversation.id, content="You are a cool agent"
            )
            session.add(m1)
            session.commit()
            print(m1.id)

            m2 = Message(conversation.id, role="user", content="Hello!")
            session.add(m2)
            session.commit()
            print(m2.id)

            print(m2.to_openai_format())

            print(conversation.to_openai_format())

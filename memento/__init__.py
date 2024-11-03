if __name__ == "__main__":
    from memento.models import SQLModel, Conversation, Message

    from sqlmodel import create_engine, Session

    engine = create_engine("sqlite:///test.db")

    SQLModel.metadata.create_all(engine)

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

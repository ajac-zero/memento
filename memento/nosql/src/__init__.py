from memento.nosql.schemas.models import Conversation, Message
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import WriteRules, init_beanie

async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.memento
    await init_beanie(database=database, document_models=[Conversation, Message])

    await Conversation.find(Conversation.user == "Anibal").delete()

    m1 = Message(role="user", content="I hope you work!")
    m2 = Message(role="assistant", content="I do <3")

    c1 = Conversation(user="Anibal", assistant="Assistant", messages=[m1])
    print(c1.id)
    c1.messages.append(m2)

    await Conversation.insert_one(c1, link_rule=WriteRules.WRITE)

    results = await Conversation.find_one(Conversation.user == "Anibal", fetch_links=True)
    messages = results.messages
    print(messages)
    # # messages = [message.dict() for message in results.messages]
    # messages.append(m2)
    # print(messages)

    # await results.set({Conversation.messages: messages})

    # results = await Conversation.find_one(Conversation.id == "65e0cdc4d5f66e95d26121a1")
    # messages = results.id
    # print(f"Updated: {messages}")




if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# Memento: _Simple LLM Memory_

Memento is a conversation management API for llm applications. It interfaces with your SQL or NoSQL database of choice to automatically handle conversational histories, assistant configurations, user preferences, and more.

Many important AI application features are supported, such as Retrieval Augmented Generation (RAG), function/tool calling and streaming, with full async support and LLM provider agnosticism.

Memento uses SQLAlchemy and Alembic under the hood to interact with SQL databases, so any database that is supported by these libraries (PostgreSQL, MySQL, SQLite, CosmoDB, etc.) is also supported by Memento. For NoSQL databasses, Memento currently used Beanie (and Bunnet) to provide suppport for MongoDB and CosmoDB.

## Getting Started

The easiest way install Memento is by running `pip install 'memento-llm[all]'` in your terminal.

## Getting Started

With Memento, you no longer have to worry about setting up message storage logic in your application, here is how I can be integrated into your code:

```py hl_lines="5 13"
from openai import OpenAI
from memento import Memento

client = OpenAI()

### Stores message history in-memory.
memory = Memento()

@memory ### Memento provides a decorator for your LLM generation function.
def generate():
    return client.chat.completions.create(
    model="gpt-3.5-turbo",
    # messages=[    ### No longer worry about the message parameter.
    #     {"role": "user", "content": "Extract Jason is 25 years old"},
    # ],
    )

response_1 = generate("My name is Anibal")
print(response_1) # Output: Hello Anibal!

response_2 = generate("What´s my name?")
print(response_2) # Output: Your name is Anibal.
```

# Memento: _Simple LLM Memory_

Memento is a conversation management API for llm applications. It interfaces with your SQL database of choice to handle conversational histories.

Memento uses SQLAlchemy and Alembic under the hood to interact with SQL databases, so any database that is supported by these libraries (PostgreSQL, MySQL, SQLite, CosmoDB, etc.) is also supported by Memento.

## Installation

```bash
$ pip install memento-llm
```

## Getting Started

With Memento, you no longer have to worry about setting up message storage logic in your application, allowing for a seamlessly stateless flow, here is how it can be integrated into your code:

### Recorder API

Currently Memento only has the `Recorder` API, which serves as a simple way to use Memento in applications dependent on SQLAlchemy sessions. Because of this fact, it is a natural fit for FastAPI applications (which is my main use for Memento, personally).

The main differentiator of the Recorder API is that it requires that a SQLAlchemy `Session` or `AsyncSession` be provided. The same base Recorder class has methods to use both types of sessions.

```py hl_lines="5 13"
from openai import OpenAI
from memento import Recorder, crud, models
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Setup

client = OpenAI()
engine = create_engine("sqlite://") # In-memory sqlite database

models.Base.metadata.create_all(engine) # For demo purposes, create tables with the metadata API

with Session(engine) as session:
  conversation_id = crud.create_conversation(session, "Testbot") # Name of the assistant/agent/app

# Usage

def generate():
  # Start the recorder with previous conversation data (Empty the during the first call, one message during the second)
  recorder = Recorder.from_conversation(session, conversation_id)

  # Call the LLM API with data retrieved from the recorder
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=recorder.to_openai_format()
  )

  # Add the response to the recorder
  recorder.add_openai_response(response)

  # Commit new messages to your database
  recorder.commit_new_messages(session)

response_1 = generate("My name is Anibal")
print(response_1) # Output: Hello Anibal!

response_2 = generate("What´s my name?")
print(response_2) # Output: Your name is Anibal.
```

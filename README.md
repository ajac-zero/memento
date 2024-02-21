# Memento

_Simple LLM Memory._

---

Memento automatically manages your conversations with LLMs with just 3 lines of code. It leverages SQLAlchemy and Alembic to store conversations between users and assistants in SQLite3 or in memory.

## Getting Started

To install Memento, run `pip install memento-llm` in your terminal.

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

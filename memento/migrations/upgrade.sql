CREATE TABLE memento_conversation (
    agent VARCHAR NOT NULL, 
    uuid CHAR(32) NOT NULL, 
    id INTEGER NOT NULL, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME, 
    archived BOOLEAN NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_memento_conversation_uuid ON memento_conversation (uuid);

CREATE TABLE memento_message (
    conversation_id INTEGER NOT NULL, 
    role VARCHAR NOT NULL, 
    content VARCHAR, 
    tools VARCHAR, 
    feedback BOOLEAN, 
    uuid CHAR(32), 
    origin_message_id INTEGER, 
    id INTEGER NOT NULL, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME, 
    archived BOOLEAN NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(conversation_id) REFERENCES memento_conversation (id), 
    FOREIGN KEY(origin_message_id) REFERENCES memento_message (id)
);

CREATE INDEX ix_memento_message_uuid ON memento_message (uuid);

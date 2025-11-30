import sqlite3
import os
from typing import List, Dict

DATABASE_NAME = 'events'
def connect():
    conn = sqlite3.connect(f'{DATABASE_NAME}.db')
    return conn

def create_tables():
    conn = connect()
    cur = conn.cursor()

    query = '''
    CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    time VARCHAR(5) NOT NULL,
    UNIQUE(name)
    )
    '''
    cur.execute(query)

    query = '''
    CREATE TABLE queries (
    event_id INTEGER,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(4) NOT NULL CHECK (type IN ('text', 'bool')),

    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE(event_id, id)
    )
    '''
    cur.execute(query)

    query = '''
    CREATE TABLE entries (
    event_id INTEGER,
    query_id INTEGER PRIMARY KEY AUTOINCREMENT,

    date VARCHAR(8) NOT NULL,
    input TEXT,

    UNIQUE(event_id, query_id, date),
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (query_id) REFERENCES queries(id)
    )
    '''
    cur.execute(query)

    conn.commit()
    conn.close()

def destroy_database():
    if os.path.exists(f'{DATABASE_NAME}.db'):
        os.remove(f'{DATABASE_NAME}.db')

if __name__ == "__main__":
    destroy_database() 
    create_tables()


def insert_event(name: str, time: str, queries: List[Dict]):
    conn = connect()
    cur = conn.cursor()

    event_query ='''
        INSERT INTO events (name, time)
        VALUES (?, ?)
    '''
    event_values = (name, time)
    cur.execute(event_query, event_values)
    event_id = cur.lastrowid

    for query in queries:
        # :)
        query_query = '''
            INSERT INTO queries (event_id, name, type)
            VALUES (?, ?, ?)
        '''
        query_values = (event_id, query['name'], query['type'])
        cur.execute(query_query, query_values)

    conn.commit()
    conn.close()


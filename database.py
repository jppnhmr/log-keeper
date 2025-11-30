import sqlite3
from typing import List, Dict

DATABASE_NAME = 'events'
def connect():
    conn = sqlite3.connect(f'{DATABASE_NAME}.db')
    return conn

def create_tables():
    conn = connect()
    cur = conn.cursor()

    query = '''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE,
        time VARCHAR(5)) NOT NULL
    )
    '''
    cur.execute(query)

    query = '''
    CREATE TABLE IF NOT EXISTS queries (
        event_id INTEGER,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL,
        type VARCHAR(4)) NOT NULL CHECK (type IN ('text', 'bool')),

        FOREIGN KEY (event_id) REFERENCES events(id),
        UNIQUE(event_id, id)
    )
    '''
    cur.execute(query)

    query = '''
    CREATE TABLE IF NOT EXISTS entries (
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

if __name__ == "__main__":

    create_tables()


def insert_event(name: str, time: str, queries: List[Dict]):
    conn = connect()
    cur = conn.cursor()

    event_query ='''
        INSERT OR IGNORE INTO events (name)
        VALUES (?, ?)
    '''
    event_values = (name, time)
    cur.execute(event_query, event_values)

    for query in queries:
        # :)
        query_query = '''
            INSERT OR IGNORE INTO events (name)
            VALUES (?, ?)
        '''
        query_values = (query['date'], query['time'])
        cur.execute(query_query, query_values)

    conn.commit()
    conn.close()


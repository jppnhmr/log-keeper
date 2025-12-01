import sqlite3
import os
from datetime import datetime
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
    time INTEGER NOT NULL,
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

    FOREIGN KEY (event_id) REFERENCES events(id)
    );
    '''
    cur.execute(query)

    query = '''
    CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    query_id INTEGER NOT NULL,
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


def insert_event(name: str, time: int, queries: List[Dict]):
    conn = connect()
    cur = conn.cursor()

    event_query ='''
        INSERT OR IGNORE INTO events (name, time)
        VALUES (?, ?)
    '''
    event_values = (name, time)
    cur.execute(event_query, event_values)
    event_id = cur.lastrowid

    if event_id != 0: # if failed to added event, skip this
        for query in queries:
            # :)
            query_query = '''
                INSERT OR IGNORE INTO queries 
                    (event_id, name, type)
                VALUES (?, ?, ?);
            '''
            query_values = (event_id, query['name'], query['type'])
            cur.execute(query_query, query_values)

    conn.commit()
    conn.close()

def get_events():
    conn = connect()
    cur = conn.cursor()

    query = '''
    SELECT id, time FROM events
    '''
    cur.execute(query)
    data = cur.fetchall()

    conn.close()
    return data 

def get_untriggered_events():
    conn = connect()
    cur = conn.cursor()

    # Select events where no entries exist for today's date
    query = '''
    SELECT e.id, e.time
    FROM events e
    LEFT JOIN entries en 
    ON e.id = en.event_id AND en.date = ?
    WHERE en.event_id IS NULL;
    '''
    values = (datetime.now().strftime('%d%m%Y'),)
    cur.execute(query, values)
    events = cur.fetchall()

    conn.close()
    return events

def get_event_queries(event_id):
    conn = connect()
    cur = conn.cursor()

    query = '''
    SELECT id, name, type
    FROM queries
    WHERE event_id = ?;
    '''
    values = (event_id,)
    cur.execute(query, values)

    data = cur.fetchall()
    queries = []
    for d in data:
        queries.append(
            {'id': d[0],
             'name': d[1],
             'type': d[2]})

    conn.close()
    return queries

def insert_entry(event_id, query_id, input):
    conn = connect()
    cur = conn.cursor()

    today = datetime.now().strftime('%d%m%Y')

    query = '''
    INSERT INTO 
    entries (event_id, query_id, date, input)
    VALUES (?, ?, ?, ?);
    '''
    values = (event_id, query_id, today, str(input))
    cur.execute(query, values)

    conn.commit()
    conn.close()

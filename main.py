from rich.console import Console
from rich.panel import Panel

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

import database as db

STYLE = 'white on blue'

def fancy_input(text, title):
    con = Console()
    con.print(Panel(
        text,
        title=title,
        style=STYLE,
        expand=False,
    ))
    return input('>> ')

import schedule
import time
from datetime import datetime

def create_event():

    name = fancy_input('Provide a name for the event', 'Create Event')
    time = fancy_input('At what time will the even trigger?', 'Create Event')
    num_queries = int(fancy_input('How many queries?', 'Create Event'))

    queries = []
    for i in range(num_queries):
        q_name = fancy_input(f'Enter the query name', f'Create Query {i}')
        q_type = fancy_input(f'Enter the query type', f'Create Query {i}')
        queries.append({'name': q_name, 'type':q_type})

    # Add to database
    db.insert_event(name, time, queries)

def check_time():
    '''
    Check database for events that can be triggered

    return List[]
    '''

    # Get all event_ids + times, that haven't triggred today
    events = db.get_untriggered_events()

    # Create list of events to trigger
    now = datetime.now().time()
    now = int(str(now.hour) + str(now.minute))

    trig_events = []
    for id, time in events:
        if time <= now:
            trig_events.append(id)

    return trig_events
    

def run_event(event):
    pass

if __name__ == "__main__":

    #create_event()
    db.insert_event('wake up', 730, 
        [{'name': 'dream journal', 'type': 'text'},
         {'name': 'dream tarcker', 'type': 'bool'}])
    
    db.insert_event('mid-day', 1300, 
        [{'name': 'day journal', 'type': 'text'},
         {'name': 'meditation tracker', 'type': 'bool'}])
    
    
    db.insert_event('wind down', 2100, 
        [{'name': 'day journal', 'type': 'text'},
         {'name': 'meditation tracker', 'type': 'bool'}])
    
    print(check_time())

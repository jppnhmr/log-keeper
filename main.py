from rich.console import Console
from rich.panel import Panel

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

from database import insert_event

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

    name = fancy_input('Provide a name for the query', 'Create Event')
    time = fancy_input('At what time will the even trigger?', 'Create Event')
    num_queries = int(fancy_input('How many queries?', 'Create Event'))

    queries = []
    for i in range(num_queries):
        q_name = fancy_input(f'Enter the query name', f'Create Query {i}')
        q_type = fancy_input(f'Enter the query type', f'Create Query {i}')
        queries.append({'name': q_name, 'type':q_type})

    # Add to database
    insert_event(name, time, queries)

def check_time():
    '''
    Check database for events that can be triggered

    return List[]
    '''

if __name__ == "__main__":

    create_event()
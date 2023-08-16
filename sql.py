import sqlite3
import json

def create_tables():
    '''
        Called the first time the program is run to create all the tables
    ''' 
    
    connection = sqlite3.connect('database.db') 
    cursor = connection.cursor()

    # Table holding every event name
    create_events_table_query = '''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT UNIQUE
    );
    '''

    # Table holding every bookmaker name
    create_bookmakers_table_query = '''
    CREATE TABLE IF NOT EXISTS bookmakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bookmaker_name TEXT UNIQUE
    );
    '''

    # Table holding all odds for all existing event-bookmaker combinations
    create_odds_table_query = '''
    CREATE TABLE IF NOT EXISTS odds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER,
        bookmaker_id INTEGER,
        team1_odds REAL,
        draw_odds REAL,
        team2_odds REAL,
        FOREIGN KEY (event_id) REFERENCES events(id),
        FOREIGN KEY (bookmaker_id) REFERENCES bookmakers(id)
    );
    '''

    cursor.execute(create_events_table_query)
    cursor.execute(create_bookmakers_table_query)
    cursor.execute(create_odds_table_query)

    connection.commit()
    connection.close()


def insert_event(event_name):
    '''
        Adds event to table if it hasn't been added already
    '''

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    insert_event_query = '''
    INSERT OR IGNORE INTO events (event_name)
    VALUES (?);
    '''

    cursor.execute(insert_event_query, (event_name,))
    connection.commit()
    connection.close()

def insert_bookmaker(bookmaker_name):
    '''
        Adds bookmaker to table if it hasn't been added already
    '''

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    insert_bookmaker_query = '''
    INSERT OR IGNORE INTO bookmakers (bookmaker_name)
    VALUES (?);
    '''

    cursor.execute(insert_bookmaker_query, (bookmaker_name,))
    connection.commit()
    connection.close()

def insert_or_update_odds(event_name, bookmaker_name, team1_odds, draw_odds, team2_odds):
    '''
        Adds/updates odds information to table if it hasn't been added already
    '''

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Get event id from events table
    event_id = cursor.execute('SELECT id FROM events WHERE event_name = ?', (event_name,)).fetchone() 
    # Get bookmaker id from bookmaker table
    bookmaker_id = cursor.execute('SELECT id FROM bookmakers WHERE bookmaker_name = ?', (bookmaker_name,)).fetchone()

    if event_id and bookmaker_id:
        update_odds_query = f'''
        INSERT OR REPLACE INTO odds (id, event_id, bookmaker_id, team1_odds, draw_odds, team2_odds)
        VALUES (
            COALESCE((SELECT id FROM odds WHERE event_id = ? AND bookmaker_id = ?), NULL),
            ?,
            ?,
            ?,
            ?,
            ?
        );
        '''

        cursor.execute(update_odds_query, (event_id[0], bookmaker_id[0], event_id[0], bookmaker_id[0], team1_odds, draw_odds, team2_odds))
        connection.commit()

    connection.close()

def clear_database():
    '''
        Deletes all the tables from the database.
        Should be called every few days to reset games and not hold any old odds that occurred already
    '''

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor() 

    # List of table names to be deleted
    tables_to_delete = ['events', 'bookmakers', 'odds']

    for table_name in tables_to_delete:
        drop_table_query = f'DROP TABLE IF EXISTS {table_name}'
        cursor.execute(drop_table_query)

    connection.commit() 
    connection.close() 



def find_arbitrage_opportunities():
    '''
        Function that is used to actually find if there are any arbitrage opportunities.
        Looks through all odds in odds table. For each outcome(home wins, draw, away wins),
            it finds the best odds from bookmakers for that event.
        After finding the best odds for the event, it calculates the inverse sum to see
            if there is an arbitrage opportunity
    '''

    connection = sqlite3.connect('database.db')  
    cursor = connection.cursor() 

    cursor.execute('SELECT event_name FROM events')
    events = [row[0] for row in cursor.fetchall()]

    arbitrage_opportunities = []  # List to store arbitrage opportunities

    for event in events:
        # Select the best odds for each team winning/draw for the current event
        best_odds_query = f'''
        SELECT e.event_name, 
               (SELECT MAX(team1_odds) FROM odds WHERE event_id = e.id) AS team1_max_odds, 
               (SELECT bookmaker_name FROM odds o1 JOIN bookmakers b1 ON o1.bookmaker_id = b1.id WHERE event_id = e.id AND team1_odds = (SELECT MAX(team1_odds) FROM odds WHERE event_id = e.id)) AS team1_bookmaker,
               (SELECT MAX(draw_odds) FROM odds WHERE event_id = e.id) AS draw_max_odds,
               (SELECT bookmaker_name FROM odds o2 JOIN bookmakers bd ON o2.bookmaker_id = bd.id WHERE event_id = e.id AND draw_odds = (SELECT MAX(draw_odds) FROM odds WHERE event_id = e.id)) AS draw_bookmaker,
               (SELECT MAX(team2_odds) FROM odds WHERE event_id = e.id) AS team2_max_odds,
               (SELECT bookmaker_name FROM odds o3 JOIN bookmakers b2 ON o3.bookmaker_id = b2.id WHERE event_id = e.id AND team2_odds = (SELECT MAX(team2_odds) FROM odds WHERE event_id = e.id)) AS team2_bookmaker
        FROM events e
        WHERE e.event_name = ?
        '''
        cursor.execute(best_odds_query, (event,))
        best_odds = cursor.fetchone()

        if best_odds:
            # Calculate the sum of inverses of the best odds
            sum_of_inverses = ((1 / best_odds[1]) + (1 / best_odds[3]) + (1 / best_odds[5]))

            # Check if an arbitrage opportunity exists
            if sum_of_inverses < 1.0: 
                arbitrage_opportunity = {
                    'event': best_odds[0], # Game that has arbitrage opportunity
                    'team1_bookmaker': best_odds[2], # Best bookmaker for home winning
                    'draw_bookmaker': best_odds[4], # Best bookmaker for draw
                    'team2_bookmaker': best_odds[6], # Best bookmaker for away winning
                    'percent_profit': round((100.0/sum_of_inverses) - 100, 2), # Guaranteed profit for opportunity
                    'percent_team1': round(100.0/(sum_of_inverses * best_odds[1]), 2), # Percent to bet on home team
                    'percent_draw': round(100.0/(sum_of_inverses * best_odds[3]), 2), # Percent to bet on draw
                    'percent_team2': round(100.0/(sum_of_inverses * best_odds[5]), 2) # Percent to bet on away team
                }
                arbitrage_opportunities.append(arbitrage_opportunity)

    connection.close()

    # Print information neatly in terminal
    print(json.dumps(arbitrage_opportunities, indent=4, ensure_ascii=False))

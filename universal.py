import re
import sql

# This file contains functions that are used across multiple scraping sripts.
# They are combined here for convenience and facility of use

def convert_odds(odd_string):
    '''
        Takes in American odds as a string and returns the European odds as a float
        ex: "+200" -> 3.0
    '''

    odd_float = 1.0

    if "+" in odd_string:
        odd_float += (int(odd_string[1:])/100)
    else:
        odd_float += (1/(int(odd_string[1:])/100))

    return round(odd_float, 4)

def preprocess_team_name(team_name):
    '''
        Takes in a team name and removes common abbreviations and acronyms to standarize the team name
    '''

    abbreviations = ['FC', 'AFC', 'SC', 'CF', 'Utd', 'AC', 'DC', 'LA', 'NY', 'NYC', 'SJ', 'STL', 'MIA',
                     'ATL', 'CHI', 'DAL', 'HOU', 'MIN', 'PHI', 'POR', 'SEA', 'SLC', 'RSL', 'TOR', 'VAN',
                     'COL', 'NE', 'ORL', 'CIN', 'NSH', 'USA', 'United', 'Football Club', 'Association Football Club', 
                     'Sporting Club', 'Club de Futbol', 'Athletic Club', 'Union']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    
    for abbreviation in abbreviations:
        team_name = re.sub(rf'\b{abbreviation}\b', '', team_name, flags=re.IGNORECASE).strip()
    for number in numbers:
        team_name = re.sub(number, '', team_name, flags=re.IGNORECASE).strip()

    # Remove special characters and symbols
    team_name = re.sub(r'[^\w\s]', '', team_name)

    # Standardize spaces
    team_name = re.sub(r'\s+', ' ', team_name).strip()

    # Convert to lowercase
    team_name = team_name.lower()

    return team_name

def standarize_event(team1, team2):
    '''
        Takes in 2 team names and standarizes the event name
    '''

    return f"{preprocess_team_name(team1)} vs {preprocess_team_name(team2)}"

def add_game_to_db(game_info):
    '''
        Takes in a dictionary of information related to a game, and adds the info to the database
    '''

    sql.insert_event(game_info.get("event", ""))
    sql.insert_or_update_odds(game_info.get("event", ""), game_info.get("book", ""), 
                              game_info.get("home", 1.0), game_info.get("draw", 1.0), game_info.get("away", 1.0))
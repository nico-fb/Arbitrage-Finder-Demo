from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import sql
import json
import time
import random
import universal as unv

def soccer(dr):
    '''
        Scrapes the soccer game odds from the BetRivers website
    '''

    url = "https://nj.betrivers.com/?page=sportsbook&group=1000093190&type=prematch"

    time.sleep(2.2)

    dr.get(url)

    time.sleep(3.1)

    # Site split up into countries (sections) and then again into leagues for each country
    # When a section is opened, it also opens the first league
    section_tabs = dr.find_elements(By.XPATH, '//*[@id="rsi-sports-feed"]/div/div/div[2]/div')

    for section_i in range(len(section_tabs)):
        time.sleep(random.randint(5,10)/10)
        # For ease of use
        section = section_tabs[section_i]

        section_button = section.find_element(By.TAG_NAME, 'button')
        section_name = section_button.get_attribute('aria-label')
        # Click section as long as it isn't the first one (since it's already open)
        if section_i != 0:
            time.sleep(random.randint(5,10)/10)
            section_button.click()

        # Get all leagues for section
        league_tabs = section.find_elements(By.XPATH, './div/div')
        for league_j in range(len(league_tabs)):
            time.sleep(random.randint(2,6)/10)
            # For ease of use
            league = league_tabs[league_j]

            league_button = league.find_element(By.TAG_NAME, 'button')
            league_name = league_button.get_attribute('aria-label')
            # Click league as long as it isn't the first one (since it's already open)
            if league_j != 0 and len(league_tabs) != 1:
                time.sleep(random.randint(2,6)/10)
                league_button.click()
                time.sleep(random.randint(2,6)/10)

            # Extract html with BeautifulSoup
            soup = BeautifulSoup(league.get_attribute('innerHTML'),"html.parser")

            all_games = soup.find_all('article', class_="sc-hpBpNF hWRXWl")

            for game in all_games:
                # Store all game info in this dict
                game_info = {}
                game_info["book"] = "betrivers"

                teams = game.find_all("span", class_="sc-dGHUoD sc-fCbHNu ILHip fFHVLa")
                # Check to make sure input is valid
                if len(teams) != 2:
                    break

                game_info["event"] = unv.standarize_event(teams[0].find(text=True), teams[1].find(text=True))

                odds = game.find_all("div", class_="sc-hqMhxz bugfLi")
                # Check to make sure input is valid
                if len(odds) != 3:
                    break
                
                for i in range(3):
                    odd_float = unv.convert_odds(odds[i].find_all("li")[0].get_text())

                    if i == 0:
                        game_info["home"] = odd_float
                    elif i == 1:
                        game_info["draw"] = odd_float
                    else:
                        game_info["away"] = odd_float

                # Optional: print game_info to terminal
                # print(json.dumps(game_info, indent=4, ensure_ascii=False))

                # Add game info to database
                unv.add_game_to_db(game_info)

            print(f"{league_name} finished")
            # Close league tab
            if len(league_tabs) != 1:
                time.sleep(random.randint(2,6)/10)
                league_button.click()


        time.sleep(random.randint(10,15)/10)
        
        # Close league tab
        section_button.click()

        print(f"SECTION: {section_name} finished")



def main(dr):
    '''
        Main function for BetRivers
        Demo only scrapes soccer odds
    '''

    # Add bookmaker name to table
    sql.insert_bookmaker("betrivers")

    soccer(dr)

    print("BetRivers finished\n\n\n")
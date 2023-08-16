from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sql
import json
import time
import random
import universal as unv

def soccer(dr):
    '''
        Scrapes the soccer game odds from the DraftKings website
    '''

    url = "https://sportsbook.draftkings.com/sports/soccer"

    time.sleep(1.4)

    dr.get(url)

    time.sleep(1.3)

    # To simulate human behavior, it gets all the different league buttons and clicks on them to then extract html
    league_tabs = dr.find_elements(By.XPATH, '//*[@id="root"]/section/section[2]/div[2]/div[2]/div[2]/div/div[2]/div')
    
    for tab in league_tabs:
        time.sleep(random.randint(2,8)/10)

        # Scrolls down to the tab so it can click on it
        dr.execute_script("return arguments[0].scrollIntoView(true);", tab)
        dr.execute_script("window.scrollBy(0, -100);")

        time.sleep(random.randint(2,10)/10)

        # Open link in new tab
        ActionChains(dr).key_down(Keys.COMMAND).click(tab).key_up(Keys.COMMAND).perform()

        time.sleep(random.randint(20,30)/10)

        # Switch tabs
        dr.switch_to.window(dr.window_handles[1])

        time.sleep(random.randint(5,10)/10)

        # Extract html with BeautifulSoup
        soup = BeautifulSoup(dr.page_source,"html.parser")
        root = soup.find_all("div", class_="sportsbook-card-accordion__children-wrapper")[0]

        # Get league name for print statements
        league_name = dr.find_element(By.XPATH, '//*[@id="root"]/section/section[2]/section/div[1]/nav/ol/li[3]/h1').text

        games = root.find_all("div", class_="sportsbook-event-accordion__wrapper expanded")

        for game in games:
            # Store all game info in this dict
            game_info = {}
            game_info["book"] = "draftkings"

            teams = game.find_all(class_="sportsbook-event-accordion__title")[0].get_text().split(" vs ")
            # Check to make sure input is valid
            if len(teams) != 2:
                break

            game_info["event"] = unv.standarize_event(teams[0], teams[1])

            odds = game.find_all("li", class_="game-props-card17__cell")
            # Check to make sure input is valid
            if len(odds) != 3:
                break

            for i in range(3):
                odd_float = unv.convert_odds(odds[i].find_all("div", class_="sportsbook-outcome-cell__elements")[0].get_text())

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

        time.sleep(random.randint(2,8)/10)

        # Close tab and switch to original
        dr.close()
        dr.switch_to.window(dr.window_handles[0])

        print(f"{league_name} finished")

def main(dr):
    '''
        Main function for DraftKings
        Demo only scrapes soccer odds
    '''

    # Add bookmaker name to table
    sql.insert_bookmaker("draftkings")

    soccer(dr)

    print("DraftKings finished\n\n\n")
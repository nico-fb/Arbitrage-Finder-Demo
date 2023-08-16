from selenium import webdriver
import draftkings
import betrivers
import sql

# This is the main script that sets up the chrome driver, and scrapes all the sportsbooks
# It also sets up the database and finds arbitrage oportunities after scraping

def setup_driver():
    '''
        Sets up the chrome driver with certain preferances that make it seem to websites
        that you are not using a webdriver and is instead controlled by a human
    '''

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    dr = webdriver.Chrome(options=options)
    dr.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    dr.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    return dr

if __name__ == "__main__":
    '''
        The main function that executes everything
    '''

    # Call this whenever you want to reset the database
    # sql.clear_database()

    # Call this after clearing the database or the first time running the script
    sql.create_tables() 


    dr = setup_driver()
    dr.get("https://www.google.com/")

    draftkings.main(dr)
    betrivers.main(dr)

    dr.quit()


    # Finds the arbitrage opportunities
    sql.find_arbitrage_opportunities()

# Arbitrage-Finder-Demo
This is a demo for a program that finds arbitrage opportunities across sportsbooks

Disclaimer: Arbitrage betting is against the terms of service of most sports betting sites. 
This demo is just that: a demonstration. This program is not being used and will not be used to 
actually make bets. It is simply a proof of concept, and for educational purposes only. Use at your own risk.

This demo only illustrates the process for soccer games across 2 sportsbooks
Additionally, every oppportunity found is printed to terminal as opposed to being emailed to you
Since this is essentially a risk-free way of making money, I will not be making the complete program public
If you end up using this demo as a base for your own product, please credit me

Even though measures are taken to make the web-browsing as human-like as possible to avoid 
bot detection, all processes comply with the robots.txt file on all websites that are being scraped
The 3 main measures taken are:
    -Clicking through the website to access data as opposed to just visitig the url
    -Waiting random time intervals between actions to not seem robotic
    -Setting up the chrom driver in a way that mostly avoids bot detection


Introduction:
Arbitrage is when you bet on all possible outcomes of a game. Usually, a bookmaker has margins on events.
This means that if you add the odds for every outcome of a game, they will be above 100% (usually 
103-110 depending on how popular the game is). Since there can only be 100% of outcomes, this means
that the bookmaker will make 3-10% of all wagers on a game. However, this is only true if they are
accurate when calculating the odds. 

Every once in a while, a bookmaker will make a mistake when calculating odds. For example, in the game
teamA vs teamB, they might calculate the probabillity of teamA winning at 50% when in reality it is 60%.
If a bookmaker makes such a mistake, you can profit off of this by betting on teamA winning from this 
bookmaker, since they are giving you better odds, and bet on teamB winning from a different bookmaker.
If you add the probabilities of each team winning you get 50% + 40% = 90%, meaning that you will make a 
profit if you bet correctly on this game. Since you are betting on all possible outcomes of the match,
you have no risk of losing money and can guarantee a profit on this game.

The only catch is that bookmakers don't make mistakes often, and if they do, they will find out and update
the odds quickly. That is why you need to look at odds across lots of bookmakers and keep updating them 
if you want to realistically find consistent opportunities.


How it works:
The program has 2 main steps:
    1 - Scrape the odds data from different sportsbooks and add them to the database
    2 - Look through the database to find arbitrage opportunities

1 - The program first sets up a web driver to simulate web browsing. This is done with Selenium.
With prewritten scripts for each bookmaker, it will visit the main url for the sport it is checking
(In this case soccer). It then clicks through the website on all available soccer leagues and scrapes 
the data. This is done through BeautifulSoup. After extracting the data (bookmaker name, event name, 
team1 odds, draw odds, team2 odds), it standarizes the event name, which is done to make sure a team 
such as Inter Miami/Inter Miami CF is considered the same (this is done with over 99% accuracy in the 
testing data), and inserts the data into a database (more info on how in the sql.py file), using SQLite. 
This is done for all games across all leagues that are offered for all bookmakers. After this, the 
web driver is closed.

2 - A function in sql.py then looks through all the odds data in the database to find the best odds for
each outcome. If the percentages add up to less than 100%, it then prints out all the information about 
the arbitrage opportunity (the game, the bookmaker to use for team1 winning, the bookmaker to use
for a draw, the bookmaker to use for team2 winning, the percent of guaranteed profit you can make, 
the percent to bet on team1, the percent to bet on a draw, and the percent to bet on team2). It checks
for opportunities for every event in the database.


Conclusion:
I hope you learned something from this repo, and sports betting in general. Reach out if you have any
questions @ nicofb31@gmail.com
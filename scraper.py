from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

headers =  {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36", 
}

url = 'https://sportsbook.draftkings.com/leagues/basketball/103?category=game-lines&subcategory=game'

req = Request(url , headers=headers)

webpage = urlopen(req).read()

page_soup = BeautifulSoup(webpage, "html.parser")

def scrape():
    
    teams = page_soup.find_all("span", {"class": "event-cell__name"})
    point_ou = page_soup.find_all("span", {"class": "sportsbook-outcome-cell__line"})
    spread_ou_ml_odds = page_soup.find_all("span", {"class": "sportsbook-odds american default-color"})

    away_home = []
    nums = list(range(0,len(teams),2))
    for num in nums:
        away_home.append({'away':BeautifulSoup.get_text(teams[num]), 'home':BeautifulSoup.get_text(teams[num+1])})

    spread_ou = []
    nums = list(range(0,len(point_ou)//2,2))
    for num in nums:
        spread_ou.append({'away_spread':BeautifulSoup.get_text(point_ou[num]), 
                        'home_spread':BeautifulSoup.get_text(point_ou[num+1]),
                        'over':BeautifulSoup.get_text(point_ou[num+(len(point_ou)//2)]),
                        'under':BeautifulSoup.get_text(point_ou[num+(len(point_ou)//2)+1])})
    
    odds = []
    nums = list(range(0,len(spread_ou_ml_odds)//3,2))
    for num in nums:
        odds.append({'away_spread_odds':BeautifulSoup.get_text(spread_ou_ml_odds[num]), 
                        'home_spread_odds':BeautifulSoup.get_text(spread_ou_ml_odds[num+1]),
                        'over_odds':BeautifulSoup.get_text(spread_ou_ml_odds[num+(len(spread_ou_ml_odds)//3)]),
                        'under_odds':BeautifulSoup.get_text(spread_ou_ml_odds[num+(len(spread_ou_ml_odds)//3)+1]),
                        'ml_away_odds':BeautifulSoup.get_text(spread_ou_ml_odds[num+(len(spread_ou_ml_odds)//3)*2]),
                        'ml_home_odds':BeautifulSoup.get_text(spread_ou_ml_odds[num+(len(spread_ou_ml_odds)//3)*2+1])})

    for index in range(len(away_home)):
        away_home[index].update(spread_ou[index])
        away_home[index].update(odds[index])
    
    return away_home


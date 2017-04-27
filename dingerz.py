import httplib2
import re
import time
import datetime
from bs4 import BeautifulSoup

#Get year/month/day from time
y = time.strftime("%Y")
m = time.strftime("%m")
d = time.strftime("%d")

#set URL to access database.
basegamedayURL = "http://gd2.mlb.com/components/game/mlb/year_" + y + "/month_" + m + "/day_" + d + "/"

team_dict = {"cle": "Indians", "cha": "White Sox", "bos": "Red Sox", "nya": "Yankees", "chn": "Cubs", "sln": "Cardinals", "col": "Rockies", "sfn": "Giants", "det": "Tigers", "sdn": "Padres",
			 "hou": "Astros", "tex": "Rangers", "kca": "Royals", "min": "Twins", "lan": "Dodgers", "ari": "Diamondbacks", "mia": "Marlins", "phi": "Phillies", "nyn": "Mets", "ana": "Angels",
			 "oak": "Athletics", "sea": "Mariners", "pit": "Pirates", "mil": "Brewers", "tba": "Rays", "cin": "Reds", "tor": "Blue Jays", "bal": "Orioles", "was": "Nationals", "atl": "Braves",
			 "asu":"Arizona State","boc":"Boston College","neu":"Northeastern University","umi":"University of Miami"}


def find_stl(text):
	return re.compile("gid").search(text) and re.compile("slnmlb").search(text)

#get games from the url
def get_games(gamedayURL):
    conn = httplib2.Http(".cache")
    page = conn.request(gamedayURL,"GET")
    page[0]
    soup = BeautifulSoup(page[1], "html.parser")
    games = [gamedayURL + game.lstrip() for game in soup.find_all(text=find_stl)]
    return games

#get all games that are in progress from the URL
def cards_games_in_progress(gamedayURL):
    conn = httplib2.Http(".cache")
    page = conn.request(gamedayURL + "scoreboard.xml","GET")
    page[0]
    soup = BeautifulSoup(page[1], "html.parser")
    count = 0
    for game in soup.find_all("game"):
        #if game["status"] == "IN_PROGRESS" or game["status"] == "PRE_GAME" or game["status"] == "IMMEDIATE_PREGAME" or game["status"] == "DELAYED":
		#TODO: CHANGE FROM FINAL TO COMMENT ABOVE
        if re.compile("slnmlb").search(game["id"]) and game["status"] == "FINAL":
            count += 1
    return count

def is_home_team(gameURL):
	conn = httplib2.Http(".cache")
	page = conn.request(gameURL + "game.xml", "GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")
	for team in soup.find_all("team"):
		if team["type"] == "home" and team["code"] == "sln":
			return True
	return False

def get_events(gameURL):
	conn = httplib2.Http(".cache")
	page = conn.request(gameURL + "game_events.xml", "GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")
	events = [load_events(bat) for bat in soup.find_all("atbat")]
	for e in events:
		x = get_more_info(gameURL, e)
		e["batter"] = x["batter"]
		e["enemy"] = x["enemy"]
		e["game_id"] = x["game_id"]
		e["pitcher"] = x["pitcher"]
	return events

def get_more_info(gameURL, event):
	conn = httplib2.Http(".cache")
	page = conn.request(gameURL + "boxscore.xml","GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")

	d = {}
	d["batter"] = " "
	d["enemy"] = " "
	d["game_id"] = " "
	d["pitcher"] = " "

	for batter in soup.find_all("batter"):
		if(batter["id"] == event["batter_no"]):
			d["game_id"] = batter.parent.parent.get("game_id")
			if batter.parent.parent.get("game_id").endswith("2"):
			    d["batter"] = batter.get("name_display_first_last") + " (game 2)"
			else:
			    d["batter"] = batter.get("name_display_first_last")
			if batter.parent.get("team_flag") == "home":
				d["enemy"] = team_dict[batter.parent.parent.get("away_team_code")]
			else:
				d["enemy"] = team_dict[batter.parent.parent.get("home_team_code")]

	for pitch in soup.find_all("pitcher"):
		if(pitch["id"] == event["pitcher_no"]):
			d["pitcher"] = pitch.get("name")
	return d

def load_events(event):
	d = {}
	d["event"] = event.get("event")
	d["event_num"] = event.get("event_num")
	d["inning"] = event.parent.parent.get("num")
	d["inning_half"] = event.parent.name
	d["batter_no"] = event.get("batter")
	d["pitcher_no"] = event.get("pitcher")
	if(event.get("event") == "Home Run"):
		d["rbi"] = event.get("rbi")
	return d

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

teamDict = {"cle": "Indians", "cha": "White Sox", "bos": "Red Sox", "nya": "Yankees", "chn": "Cubs", "sln": "Cardinals", "col": "Rockies", "sfn": "Giants", "det": "Tigers", "sdn": "Padres",
			 "hou": "Astros", "tex": "Rangers", "kca": "Royals", "min": "Twins", "lan": "Dodgers", "ari": "Diamondbacks", "mia": "Marlins", "phi": "Phillies", "nyn": "Mets", "ana": "Angels",
			 "oak": "Athletics", "sea": "Mariners", "pit": "Pirates", "mil": "Brewers", "tba": "Rays", "cin": "Reds", "tor": "Blue Jays", "bal": "Orioles", "was": "Nationals", "atl": "Braves",
			 "asu":"Arizona State","boc":"Boston College","neu":"Northeastern University","umi":"University of Miami"}


def findStl(text):
	return re.compile("gid").search(text) and re.compile("slnmlb").search(text)

#get games from the url
def getGames(gamedayURL):
	conn = httplib2.Http(".cache")
	page = conn.request(gamedayURL,"GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")
	games = [gamedayURL + game.lstrip() for game in soup.find_all(text=findStl)]
	return games

def findStlID(text):
	return re.compile("slnmlb").search(text)

def findStatus(text):
	return re.compile("IN_PROGRESS").search(text) or re.compile("IMMEDIATE_PREGAME").search(text) or re.compile("DELAYED").search(text)

def findCompleteStatus(text):
	return re.compile("FINAL").search(text) or re.compile("GAME_OVER").search(text)

#get all games that are in progress from the URL
def cardsGamesInProgress(gamedayURL):
	conn = httplib2.Http(".cache")
	page = conn.request(gamedayURL + "scoreboard.xml","GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")
	games = soup.find_all("game", id=findStlID, status=findStatus)
	for game in games:

		game["cards_score"] = " "
		game["enemy_score"] = " "
		game["inning"] = " "
		if re.compile("slnmlb").search(game["id"]) and (game["status"] == "IN_PROGRESS" or game["status"] == "IMMEDIATE_PREGAME" or game["status"] == "DELAYED"):
			team1 = game.parent.findNext("team")
			if team1["name"] == "Cardinals":
				game["cards_score"] = team1.find("gameteam").get("r")
				game["enemy_name"] = team1.findNext("team").get("name")
				game["enemy_score"] = team1.findNext("team").find("gameteam").get("r")
			else:
				game["enemy_name"] = team1.get("name")
				game["enemy_score"] = team1.find("gameteam").get("r")
				game["cards_score"] = team1.findNext("team").find("gameteam").get("r")
			for child in team1.parent.children:
				if child.name == "inningnum":
					game["inning"] = child.get("inning")
		else:
			games.remove(game)
	return games

#get all games that are in progress from the URL
def cardsGamesCompleted(gamedayURL):
	conn = httplib2.Http(".cache")
	page = conn.request(gamedayURL + "scoreboard.xml","GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")
	games = soup.find_all("game", id=findStlID, status=findCompleteStatus)
	for game in games:

		game["cards_score"] = " "
		game["enemy_score"] = " "
		game["inning"] = " "
		if re.compile("slnmlb").search(game["id"]) and (game["status"] == "FINAL" or game["status"] == "GAME_OVER"):
			team1 = game.parent.findNext("team")
			if team1["name"] == "Cardinals":
				game["cards_score"] = team1.find("gameteam").get("r")
				game["enemy_name"] = team1.findNext("team").get("name")
				game["enemy_score"] = team1.findNext("team").find("gameteam").get("r")
			else:
				game["enemy_name"] = team1.get("name")
				game["enemy_score"] = team1.find("gameteam").get("r")
				game["cards_score"] = team1.findNext("team").find("gameteam").get("r")
			for child in team1.parent.children:
				if child.name == "inningnum":
					game["inning"] = child.get("inning")
		else:
			games.remove(game)
	return games

def isHomeTeam(gameURL):
	conn = httplib2.Http(".cache")
	page = conn.request(gameURL + "game.xml", "GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")
	for team in soup.find_all("team"):
		if team["type"] == "home" and team["code"] == "sln":
			return True
	return False

def getScore(gameURL):
	conn = httplib2.Http(".cache")
	page = conn.request(gaemURL + "game_events.xml", "GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")
	games = []

def getEvents(gameURL):
	conn = httplib2.Http(".cache")
	page = conn.request(gameURL + "game_events.xml", "GET")
	page[0]
	soup = BeautifulSoup(page[1], "html.parser")
	events = [loadEvents(bat) for bat in soup.find_all("atbat")]
	for e in events:
		x = getMoreInfo(gameURL, e)
		e["batter"] = x["batter"]
		e["enemy"] = x["enemy"]
		e["game_id"] = x["game_id"]
		e["pitcher"] = x["pitcher"]
	return events

def getMoreInfo(gameURL, event):
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
				d["enemy"] = teamDict[batter.parent.parent.get("away_team_code")]
			else:
				d["enemy"] = teamDict[batter.parent.parent.get("home_team_code")]

	for pitch in soup.find_all("pitcher"):
		if(pitch["id"] == event["pitcher_no"]):
			d["pitcher"] = pitch.get("name")
	return d

def loadBatters(batter):
	if batter.parent.parent.get(batter.parent.get("team_flag") + "_team_code") == "sln":
		d = {}
		d["id"] = batter.get("id")
		d["batter"] = batter.get("name_display_first_last")
		d["s_hr"] = batter.get("s_hr")
		return d
	else:
		return None

def getBatters(gameURL):
    conn = httplib2.Http(".cache")
    page = conn.request(gameURL + "boxscore.xml","GET")
    page[0]
    soup = BeautifulSoup(page[1], "html.parser")
    batters = [loadBatters(batter) for batter in soup.find_all("batter")]
    batters = getCareer(gameURL, batters)
    return batters

def getCareer(gameURL, batters):
	batters = [bat for bat in batters if bat is not None]
	for bat in batters:
		if(bat is not None and bat != 0):
			conn = httplib2.Http(".cache")
			page = conn.request(gameURL + "batters/" + bat["id"] + ".xml","GET")
			page[0]
			soup = BeautifulSoup(page[1], "html.parser")
			bat["c_hr"] = soup.find("career").get("hr")
	return batters

def loadEvents(event):
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

import sys
from dingerz import *
import sqlite3 as sql

def check_4_dingerz():

	dbConn = sql.connect("test.db")

	if(cards_games_in_progress(basegamedayURL) != 0):
		print "There is a game in progress"
		todays_games = get_games(basegamedayURL)
		for x in range(0,len(todays_games)):
			game_events = get_events(todays_games[x])
			for event in game_events:
				inning_half = "bottom"
				if(not is_home_team(todays_games[x])):
					inning_half = "top"

				if(event["event"] == "Home Run" and event["inning_half"] == inning_half):
					gameID = event["game_id"]
					eventID = event["event_num"]
					row = " "
					with dbConn:
						cur = dbConn.cursor()
						cur.execute("SELECT * FROM Home_runs WHERE Game_ID=:gID AND Event_ID=:eID", {"gID" : gameID, "eID" : eventID})
						row = cur.fetchone()

					if(row != None):
						print "Home run from " + event["batter"] + " already tweeted"
					else:
						print event["batter"] + " hits a HOME RUN against the " + event["enemy"]
						with dbConn:
							cur = dbConn.cursor()
							cur.execute("INSERT INTO Home_runs VALUES(?, ?, ?, ?, ?, ?, ?)", (
							event["game_id"], event["event_num"], event["batter_no"], event["batter"],
							event["pitcher_no"], event["pitcher"], event["rbi"]
							));

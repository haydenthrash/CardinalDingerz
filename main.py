import sys
from dingerz import *
from DB import *
from tweeter import *
import sqlite3 as sql

def check_4_dingerz():

	#TODO:
	# Add differing tweets
	# Add foreign key between games (if gameID is the same for Inning_Scores and Home_runs)
	# X Add scores at 3rd, 6th, 9th, each EI and end of game
		#NEEDS TO BE TESTED (mainly extra innings)

	dbConn = sql.connect("test.db")

	inProgressGames = cards_games_in_progress(basegamedayURL)
	if(len(inProgressGames) != 0):

		print "There are %d game(s) in progress" % (len(inProgressGames))
		todays_games = get_games(basegamedayURL)
		for prog in inProgressGames:
			if(not isScoreInDB(prog["id"], prog["inning"], dbConn)):
				addScoreToDB(prog, dbConn)
				print "Cards: " + prog["cards_score"]
				print prog["enemy_name"]+ " " + prog["enemy_score"]
		for x in range(0,len(todays_games)):

			game_events = get_events(todays_games[x])
			for event in game_events:

				inning_half = "bottom"
				if(not is_home_team(todays_games[x])):
					inning_half = "top"

				if(event["event"] == "Home Run" and event["inning_half"] == inning_half):

					gameID = event["game_id"]
					eventID = event["event_num"]

					batters = get_batters(todays_games[x])
					for bat in batters:
						insertBatter(bat, dbConn)
						if(bat["id"] == event["batter_no"]):
							event["s_hr"] = bat["s_hr"]
							event["c_hr"] = bat["c_hr"]

					if(not isHRinDB(gameID, eventID, dbConn)):
						tweet_event(event)
						insertEvent(event, dbConn)

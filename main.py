import sys
from dingerz import *
from DB import *
from tweeter import *
import sqlite3 as sql

def check4Dingerz():

	#TODO:
	# Add differing tweets

	dbConn = sql.connect("test.db")

	inProgressGames = cardsGamesInProgress(basegamedayURL)
	completedGames = cardsGamesCompleted(basegamedayURL)
	cardsScore = 0
	enemyScore = 0

	if(len(inProgressGames) != 0):
		print "There are %d game(s) in progress" % (len(inProgressGames))
		todaysGames = getGames(basegamedayURL)
		for prog in inProgressGames:
			cardsScore = prog["cards_score"]
			enemyScore = prog["enemy_score"]
			if(not isScoreInDB(prog["id"], prog["inning"], dbConn)):
				#Don't want to even check if its not 3,6,9 or extra.
				inningNo = prog["inning"]
				if int(inningNo) != 3 and int(inningNo) != 6 and int(inningNo) < 9:
					pass

				else:
					addScoreToDB(prog, dbConn)
					tweetScores(prog)
		for x in range(0,len(todaysGames)):
			gameEvents = getEvents(todaysGames[x])
			for event in gameEvents:

				inningHalf = "bottom"
				if(not isHomeTeam(todaysGames[x])):
					inningHalf = "top"
					print("away team")

				if(event["event"] == "Home Run" and event["inning_half"] == inningHalf):
					gameID = event["game_id"]
					eventID = event["event_num"]
					event["cards_score"] = cardsScore
					event["enemy_score"] = enemyScore

					batters = getBatters(todaysGames[x])
					for bat in batters:
						if(not batterInDB(bat["id"], dbConn)):
							insertBatter(bat, dbConn)

						if(bat["id"] == event["batter_no"]):
							event["s_hr"] = bat["s_hr"]
							event["c_hr"] = bat["c_hr"]

					if(not isHRinDB(gameID, eventID, dbConn)):
						increaseHR(event["batter_no"], event["s_hr"], event["c_hr"],dbConn)
						tweetEvent(event)
						insertEvent(event, dbConn)
	if(len(completedGames) != 0):
		for game in completedGames:
			if(not isFinalInDB(game["id"], dbConn)):
				game["num_hrs"] = getGameHRS(game["id"], dbConn)
				addFinalToDB(game, dbConn)
				tweetFinalScore(game)

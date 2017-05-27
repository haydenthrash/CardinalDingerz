import sqlite3 as sql
import sys


def batterInDB(batID, dbConn):

	with dbConn:
		current = dbConn.cursor()
		current.execute("SELECT * FROM Cardinal_Batters WHERE Batter_ID=:bId", {"bId":batID})
		data = current.fetchone()

		if(data == None):
			return False
		else:
			return True

def insertBatter(batter, dbConn):
	if(not batterInDB(batter["id"], dbConn)):
		with dbConn:
			current = dbConn.cursor()
			current.execute("INSERT INTO Cardinal_Batters VALUES (?, ?, ?, ?)", (batter["id"], batter["batter"], batter["s_hr"], batter["c_hr"]))

def increaseHR(batterID, dbConn):
	with dbConn:
		current = dbConn.cursor()
		current.execute("UPDATE Cardinal_Batters SET Season_HRS = Season_HRS + 1 WHERE Batter_ID=:bId", {"bId":batterID})
		current.execute("UPDATE Cardinal_Batters SET Career_HRS = Career_HRS + 1 WHERE Batter_ID=:bId", {"bId":batterID})

def isHRinDB(gameID, eventID, dbConn):
	with dbConn:
		cur = dbConn.cursor()
		cur.execute("SELECT * FROM Home_runs WHERE Game_ID=:gID AND Event_ID=:eID", {"gID" : gameID, "eID" : eventID})
		row = cur.fetchone()

	if(row == None):
		return False
	else:
		return True

def insertEvent(event, dbConn):
	with dbConn:
		cur = dbConn.cursor()
		cur.execute("INSERT INTO Home_runs VALUES(?, ?, ?, ?, ?, ?, ?)", (
		event["game_id"], event["event_num"], event["batter_no"], event["batter"],
		event["pitcher_no"], event["pitcher"], event["rbi"]
		));

def isScoreInDB(gameID, inningNo, dbConn):
	with dbConn:
		cur = dbConn.cursor()
		cur.execute("SELECT * FROM Inning_Scores WHERE Game_ID=:gID AND Inning_No=:iNo", {"gID": gameID, "iNo": inningNo})
		row = cur.fetchone()

	if(row == None):
		return False
	else:
		return True

def addScoreToDB(gameScore, dbConn):
	with dbConn:
		cur = dbConn.cursor()
		cur.execute("INSERT INTO Inning_Scores VALUES(?, ?, ?, ?, ?)", (
		gameScore["id"], gameScore["inning"], gameScore["cards_score"], gameScore["enemy_score"], gameScore["enemy_name"]
		))

def isFinalInDB(gameID, dbConn):
	with dbConn:
		cur = dbConn.cursor()
		cur.execute("SELECT * FROM Final_Scores WHERE Game_ID=:gID", {"gID": gameID})
		row = cur.fetchone()

		if(row == None):
			return False
		else:
			return True
def addFinalToDB(game, dbConn):
	with dbConn:
		cur = dbConn.cursor()
		cur.execute("INSERT INTO Final_Scores VALUES(?, ?, ?, ?, ?)", (
		game["id"], game["enemy_name"], game["cards_score"], game["enemy_score"], game["num_hrs"]
		))

def getGameHRS(gameID, dbConn):
	with dbConn:
		cur = dbConn.cursor()
		cur.execute("SELECT * FROM Home_runs WHERE Game_ID=:gID", {"gID": gameID})
		rows = cur.fetchall()
		return len(rows)

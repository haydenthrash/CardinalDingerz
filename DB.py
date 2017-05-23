import sqlite3 as sql
import sys


def batterInDB(bat_id, dbConn):

	with dbConn:
		current = dbConn.cursor()
		current.execute("SELECT * FROM Cardinal_Batters WHERE Batter_ID=:bId", {"bId":bat_id})
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

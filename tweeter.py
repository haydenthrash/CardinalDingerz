from tweets import *
from TwitterAuth import *
import tweepy
import random

def tweetScores(game):
	auth = tweepy.OAuthHandler(ConsKey, ConsSecret)
	auth.set_access_token(AccToken, AccTokenSecret)
	twitterApi = tweepy.API(auth)
	inning = game["inning"]
	if(inning == 3):
		inning = "3rd"
	else:
		inning = str(inning) + "th"
	cardsScore = game["cards_score"]
	enemyScore = game["enemy_score"]
	enemyName = game["enemy_name"]

	tweet = ""

	if(int(cardsScore) > int(enemyScore)):
		index = random.randint(0, len(winningTweets)-1)
		tweet = winningTweets[index] % locals()
	elif(int(cardsScore) == int(enemyScore)):
		index = random.randint(0, len(tiedTweets)-1)
		tweet = tiedTweets[index] % locals()
	else:
		index = random.randint(0, len(losingTweets)-1)
		tweet = losingTweets[index] % locals()

	print tweet
	#twitterApi.update_status(status=tweet)

def tweetEvent(event):
	auth = tweepy.OAuthHandler(ConsKey, ConsSecret)
	auth.set_access_token(AccToken, AccTokenSecret)
	twitterApi = tweepy.API(auth)

	batter = event["batter"]
	enemy = event["enemy"]
	pitcher = event["pitcher"]
	rbi = event["rbi"]
	cardsScore = event["cards_score"]
	enemyScore = event["enemy_score"]
	seasonHR = event["s_hr"]
	careerHR = event["c_hr"]

	tweet = ""

	if(rbi != 4):
		index = random.randint(0, len(homeRunTweets)-1)
		tweet = homeRunTweets[index] % locals()
	else:
		tweet = "%(batter)s hits a GRAND SLAM against the %(enemy)s" % locals()
	print tweet
	#twitterApi.update_status(status=tweet)

def tweetFinalScore(game):
	auth = tweepy.OAuthHandler(ConsKey, ConsSecret)
	auth.set_access_token(AccToken, AccTokenSecret)
	twitterApi = tweepy.API(auth)

	cardsScore = game["cards_score"]
	enemyScore = game["enemy_score"]
	enemyName = game["enemy_name"]

	tweet = ""

	if(int(cardsScore) > int(enemyScore)):
		index = random.randint(0, len(winTweets)-1)
		tweet = winTweets[index] % locals()
	else:
		index = random.randint(0, len(loseTweets)-1)
		tweet = loseTweets[index] % locals()
	print tweet
	#twitterApi.update_status(status=tweet)

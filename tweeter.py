from tweets import *
from TwitterAuth import *
import tweepy
import random

def tweet_scores(game):
	auth = tweepy.OAuthHandler(ConsKey, ConsSecret)
	auth.set_access_token(AccToken, AccTokenSecret)
	twitterApi = tweepy.API(auth)
	inning = game["inning"]
	if(inning is 3):
		inning = "3rd"
	else:
		inning = str(inning) + "th"
	cardsScore = game["cards_score"]
	enemyScore = game["enemy_score"]
	enemyName = game["enemy_name"]

	index = random.randint(0, len(ScoreTweets)-1)

	tweet = ScoreTweets[index] % locals()
	print tweet
	#twitterApi.update_status(status=tweet)

def tweet_event(event):
	auth = tweepy.OAuthHandler(ConsKey, ConsSecret)
	auth.set_access_token(AccToken, AccTokenSecret)
	twitterApi = tweepy.API(auth)

	batter = event["batter"]
	enemy = event["enemy"]
	pitcher = event["pitcher"]
	rbi = event["rbi"]

	seasonHR = event["s_hr"]
	careerHR = event["c_hr"]

	tweet = ""

	if(rbi is not 4):
		index = random.randint(0, len(HomeRunTweets)-1)
		tweet = HomeRunTweets[index] % locals()
	else:
		tweet = "%(batter)s hits a GRAND SLAM against the %(enemy)s" % locals()
	print tweet
	#twitterApi.update_status(status=tweet)

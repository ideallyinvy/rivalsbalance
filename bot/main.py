import tweepy
from time import sleep
import csv, json, ftfy
import os, random

# Twitter bot for posting Rivals of Aether balance changes
# @author mjhancock
# last updated 22-5-22

if __name__ == "__main__":

	# local access file
	try:
		cred = json.load(open('./credentials.json', 'r'))
	except:
		cred = False
	
	# connect to client locally
	if cred:
		client = tweepy.Client(bearer_token=cred['bearer token'],
		consumer_key=cred['consumer key'],
		consumer_secret=cred['consumer secret'],
		access_token=cred['access token'],
		access_token_secret=cred['access token secret'])
	
	# connect to client with host access data
	else:
		bt = os.getenv('bt')
		ck = os.getenv('ck')
		cs = os.getenv('cs')
		at = os.getenv('at')
		ats = os.getenv('ats')

		client = tweepy.Client(bearer_token=bt,
		consumer_key=ck,
		consumer_secret=cs,
		access_token=at,
		access_token_secret=ats)

	# open csv with all patch notes
	with open('./allnotes.csv', mode='r', encoding='utf8') as notes:
	
		csvFile = csv.reader(notes)
		readLines = 0
		first = True
		
		# find random balance change
		for line in csvFile:
			if first:
				entries = int(line[0])
				target = random.randint(1, entries)
				first = False

			# target note found, construct tweet
			elif readLines == target:
				message = ftfy.fix_text(line[0] + " (" + line[1] + ")\n" + line[2]) 
			readLines += 1

	# post tweet
	client.create_tweet(text=message)
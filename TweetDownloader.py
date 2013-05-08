#!/usr/bin/env python
import twitter, sys, re, time

class TweetDownloader:
	def __init__(me, search_string):
		me.api = twitter.Api()
		me.search_string = search_string
		me.quoted_string = "\"" + search_string + "\""
		me.max_id = None
		me.pattern = search_string + r"[^\.\?!\n:,#]*[\.\?!]*"
		me.re = re.compile(me.pattern, flags=re.IGNORECASE)

	def process_tweet(me, tweet):
		# Uses regular expressions to simplify the tweet to contain
		# a sentance or phrase starting with the search expression
		# eg: "Argh Dan, why are you so awesome?!" with search 
		# string "why are you" goes to 
		# "why are you so awesome?!"
		# Depends on tweet having a .text and .search_string attribute
		# creates a .simpletext attribute
		# Returns True if processing is successful
		# Returns False if unable to process (e.g. RE didnt match)
		tweet.text = tweet.text.encode('utf-8', 'ignore')
		match = me.re.search(tweet.text)
		if not match:
			print "PATTERN: " + me.pattern + " NO MATCH"
			return False

		phrase = match.group()
		if phrase[-4:] == "http":
			phrase = phrase[:-4] # remove links

		tweet.phrase = phrase
		return True

	def search(me):
		results = me.api.GetSearch(me.quoted_string,
					since_id=me.max_id)
		me.max_id = max(r.id for r in results) # i <3 generators
		goodresults = [r for r in results if me.process_tweet(r)]
		for r in goodresults:
			print "~~~~~~~~~~~~~~~~~~~~~~"
			print r.phrase


def main():
	args = sys.argv
	if len(args) == 1:
		search_string = ("why am i")

	else:
		search_string = " ".join(args[1:])

	t = TweetDownloader(search_string)
	while True:
		t.search()
		time.sleep(20)


if __name__ == '__main__':
	main()
#!/usr/bin/env python
import twitter, sys, re, datetime, time, dateutil.parser, pytz
CST = pytz.timezone("US/Central")

class TweetDownloader:
	"""Downloads Tweets matching a given search string and regular expression pattern.
	TODO: Implement public interface get_Tweets(freshness) which returns all matching Tweets
	which are fewer than (freshness) seconds old.
	Takes a search string and options dictionary with parameters:
	"REQUIRE_MATCH": True  -> find regex only at start of tweet 	
					 False -> find regex anywhere in tweet
	"BLOCK_RETWEETS": True -> Block recent retweets (NOT IMPLEMENTED)
	"VERBOSE"    :  True -> Print a lot of stuff
	"TIMER"      :  True -> Print download times
	"POSTFIX" : a regular expression string to append after the search string
	"PREFIX"  : a regular expression string to prepend to the search string
	"CASE_SENSITIVE": True -> Enable case sensitivity"""

	def __init__(me, search_string, require_match=False, block_retweets=False, 
		verbose=False, timer=False, prefix="", postfix=r"[^\.\?!\n:,#]*[\.\?!]*",
		case_sensitive=False):
		me.require_match  = require_match
		me.block_retweets = block_retweets #Not implemented
		me.verbose        = verbose
		me.timer          = timer
		
		me.api = twitter.Api()
		me.search_string = search_string
		me.quoted_string = "\"" + search_string + "\""
		me.max_id = None
		me.pattern = prefix + search_string + postfix
		flags = None if case_sensitive else re.IGNORECASE
		me.re = re.compile(me.pattern, flags=flags)

	def process_Tweet(me, tweet):
		"""Uses regular expressions to simplify the tweet to contain
		 a sentance or phrase starting with the search expression
		 eg: "Argh Dan, why are you so awesome?!" with search 
		 string "why are you" goes to 
		 "why are you so awesome?!"
		 Depends on tweet having a .text and .search_string attribute
		 creates a .simpletext attribute
		 Returns True if processing is successful
		 Returns False if unable to process (e.g. RE didnt match)
		 If processing is successful, it adds attributes 
		 Tweet.phrase (the matching expression) and Tweet.time
		 (a DateTime object)"""
		tweet.text = tweet.text.encode('utf-8', 'ignore')
		if me.require_match: 
			match = me.re.match(tweet.text)
		else:
			match = me.re.search(tweet.text)

		if not match:
			if me.verbose:
				print "Failed to match: "
				print "TWEET: ", tweet.text
				print "PATTERN: ", me.pattern
			return False

		phrase = match.group()
		if phrase[-4:] == "http":
			phrase = phrase[:-4] # remove links

		tweet.phrase = phrase
		tweet.time = dateutil.parser.parse(tweet.created_at)
		return True

	def search(me):
		"""Private function which searches Twitter for new Tweets with the target phrase, and processes them to see if they 
		have a phrase matching our regular expression."""
		if TIMER: search_start = time.time()
		results = me.api.GetSearch(me.quoted_string, since_id=me.max_id)
		if TIMER: 
			download_end = time.time()
			print "Time to download: ", (download_end - search_start) * 1000, "ms ", "found:", len(results)

		if not results:
			return []

		me.max_id = max(r.id for r in results) # i <3 generators

		goodresults = [r for r in results if me.process_Tweet(r)]
		
		if me.verbose:
			print "=========================", len(results)
			for r in goodresults:
				print "~~~~~~~~~~~~~~~~~~~~~~"
				#print r.text
				print r.phrase

		return goodresults

def call_and_response():
	why = TweetDownloader("why am i", False)
	because = TweetDownloader("because you", True)
	whylist = []
	becauselist = []

	while True:
		whylist += why.search()
		becauselist += because.search()
		try:
			for i in xrange(10):
				w = whylist.pop()
				b = becauselist.pop()
				print "~~~~~~~~~~~~~~~~~~~~~~"
				print w.phrase
				time.sleep(1)
				print b.phrase
				time.sleep(2)
		except:
			time.sleep(5)

def get_exchanges(nPairs=500):
	why = TweetDownloader("why am i", False)
	because = TweetDownloader("because you", True)
	whylist = []
	becauselist = []

	start = time.time()
	whylist += why.search()
	becauselist += because.search()
	for i in xrange(nPairs):
		try:
			if not(whylist and becauselist):
				raise IndexError
				# Pop would fail on empty (false) list
			w = whylist.pop()
			b = becauselist.pop()
			print #"~~~~~~~~~~~~~~~~~~~~~~"
			print w.time.astimezone(CST).strftime("%I:%M:%S%p"),
			print ": ", w.phrase 
			print b.time.astimezone(CST).strftime("%I:%M:%S%p"),
			print ": ", b.phrase 
		except IndexError:
			whylist += why.search()
			becauselist += because.search()
			time.sleep(4)			

	end = time.time()

	print "Time elapsed: ", end-start


def main():
	args = sys.argv
	if len(args) == 1:
		get_exchanges(100)

	else:
		search_string = " ".join(args[1:])
		print search_string
		t = TweetDownloader(search_string, True)
		while True:
			t.search()
			time.sleep(20)


if __name__ == '__main__':
	main()
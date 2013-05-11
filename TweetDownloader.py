#!/usr/bin/env python
import dan_twitter as twitter
import re
import time, datetime, dateutil.parser, pytz
import argparse

CST = pytz.timezone("US/Central")

class TweetDownloader:
	"""Downloads Tweets matching a given search string and regular expression pattern.
	Implements 1 public method, get_Tweets, which will return a list of all recent Tweets
	which match the search pattern. Returns older Tweets first. Can return the same Tweets
	multiple times if called in quick succession, i.e. does not clear buffer after returning

	Takes a search string and the following options:
	"freshness" (int f)  : Guarantees that get_Tweets method will return Tweets at most 
						  	f seconds old
	"query_rate" (int q) : The maximum rate at which the Downloader will query Twitter
	"REQUIRE_MATCH"  (-r): True  -> find regex only at start of tweet 	
					 	   False -> find regex anywhere in tweet
	"BLOCK_RETWEETS" (-b): True -> Block recent retweets (NOT IMPLEMENTED)
	"VERBOSE"        (-v): True -> Print a lot of stuff
	"TIMER"          (-t): True -> Print download times
	"CASE_SENSITIVE" (-c): True -> Enable case sensitivity
	"PREFIX"             : a regular expression string to prepend to the search string
	"POSTFIX"            : a regular expression string to append after the search string"""

	def __init__(me, search_string, freshness=10, query_rate=3, require_match=False, 
		block_retweets=False, verbose=False, timer=False, prefix="", 
		postfix=r"[^\.\?!\n:,#]*[\.\?!]*", case_sensitive=False):
		me.search_string  = search_string
		me.quoted_string  = "\"" + search_string + "\""
		me.freshness      = freshness
		me.query_rate     = query_rate
		me.require_match  = require_match
		me.block_retweets = block_retweets #Not implemented
		me.verbose        = verbose
		me.timer          = timer
		me.api            = twitter.Api()
		me.max_id         = None
		me.pattern        = prefix + search_string + postfix
		flags 			  = 0 if case_sensitive else re.IGNORECASE
		me.re 			  = re.compile(me.pattern, flags=flags)

	def _process_Tweet(me, tweet):
		"""Uses regular expressions to simplify the tweet to contain
		 a sentance or phrase starting with the search expression
		 eg: "Argh Dan, why are you so awesome?!" with search 
		 string "why are you" goes to "why are you so awesome?!"
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

	def _search(me):
		"""Private function which searches Twitter for new 
		Tweets with the target string, and processes them to see if they 
		have a phrase matching our regular expression."""
		if me.timer: search_start = time.time()
		results = me.api.GetSearch(me.quoted_string, since_id=me.max_id)
		if me.timer: 
			download_end = time.time()
			print "Time to download: ", (download_end - search_start) * 1000, 
			print "ms ", "found:", len(results)

		if not results:
			return []

		me.max_id = max(r.id for r in results) # i <3 generators

		good_Tweets = [r for r in results if me._process_Tweet(r)]
		
		if me.verbose:
			print "=========================", len(results)
			for r in good_Tweets:
				print "~~~~~~~~~~~~~~~~~~~~~~"
				print r.text
				print r.phrase

		return good_Tweets



def main():
	parser = argparse.ArgumentParser("TweetDownloader")
	parser.add_argument("-r", "--require-match", dest="rm",
		help="Require regex to match on start of Tweet", action="store_true")
	parser.add_argument("-b", "--block-retweets", dest="b",
		help="Block retweets - NOT IMPLEMENTED", action="store_true")
	parser.add_argument("-v", "--verbose", dest="v",
		help="Print a lot of info", action="store_true")
	parser.add_argument("-t", "--timer", dest="t",
		help="Print download time in miliseconds", action="store_true")
	parser.add_argument("-c", "--case-sensitive", dest="c",
		help="make search string case sensitive", action="store_true")
	parser.add_argument("words", nargs="*", 
		help="the string to search for", default=["why","am","i"])

	args = parser.parse_args()


	search_string = " ".join(args.words)
	t = TweetDownloader(search_string, require_match=args.rm, block_retweets=args.b, 
		verbose=args.v, timer=args.t, prefix="", postfix=r"[^\.\?!\n:,#]*[\.\?!]*",
		case_sensitive=args.c)
	tweets = t._search()[::-1]
	while True:
		if tweets:
			for tweet in tweets:
				print tweet.time.astimezone(CST).strftime("%I:%M:%S%p"),
				print tweet.phrase
				time.sleep(1)
		else:
			tweets += t._search()[::-1]
			time.sleep(3)

if __name__ == '__main__':
	main()
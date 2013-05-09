#!/usr/bin/env python
import twitter, sys, re, time

class TweetDownloader:
	def __init__(me, search_string, search_mode = True, verbose = False):
		# SearchMode: True -> Search (phrase can be anywhere in 
		# text) False -> Match (phrase must be at start of text)
		me.api = twitter.Api()
		me.search_string = search_string
		me.quoted_string = "\"" + search_string + "\""
		me.max_id = None
		me.pattern = search_string + r"[^\.\?!\n:,#]*[\.\?!]*"
		me.re = re.compile(me.pattern, flags=re.IGNORECASE)
		me.search_mode = search_mode
		me.verbose = verbose

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
		if me.search_mode: 
			match = me.re.search(tweet.text)
		else:
			match = me.re.match(tweet.text)
		if not match:
			if me.verbose:
				print "TWEET: ", tweet.text
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
		
		if results is []:
			return []

		min_id = min(r.id for r in results)
		me.max_id = max(r.id for r in results) # i <3 generators

		goodresults = [r for r in results if me.process_tweet(r)]
		
		if me.verbose:
			print "=========================", len(results)
			for r in goodresults:
				print "~~~~~~~~~~~~~~~~~~~~~~"
				#print r.text
				print r.phrase
				#print r.id, ",", r.id - min_id
				#print r.created_at
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
			print "~~~~~~~~~~~~~~~~~~~~~~"
			print w.created_at, ": ", w.phrase 
			print b.created_at, ": ", b.phrase 
		except IndexError:
			whylist += why.search()
			becauselist += because.search()
			time.sleep(2)			

	end = time.time()

	print "Time elapsed: ", end-start




def main():
	args = sys.argv
	if len(args) == 1:
		get_exchanges(500)

	else:
		search_string = " ".join(args[1:])

		t = TweetDownloader(search_string, True)
		while True:
			t.search()
			time.sleep(20)


if __name__ == '__main__':
	main()
#!/usr/bin/env python
import twitter, sys, re

# Simple Tweet Dictionary:
# 

def phraseify(text, search_string):
	pattern = search_string + r"[^\.\?!\n:,#]*[\.\?!]*"

	match = re.search(pattern, text, flags=re.IGNORECASE)
	if not match:
		# print pattern
		# print text
		print "PATTERN: " + pattern + " NO MATCH"
		raise LookupError
	text = match.group()
	if text[-4:] == "http":
		text = text[:-4] # remove links
	return text



class TweetDownloader:
	def __init__(me, search_string):
		me.api = twitter.Api()
		me.search_string = search_string
		max_id = None
		re_pattern = search_string + r"[^\.\?!\n:,#]*[\.\?!]*"
		me.re = re.compile(re_pattern)

	def simplify_tweet(me, tweet):
		# Uses regular expressions to simplify the tweet to contain
		# a sentance or phrase starting with the search expression
		# eg: "Argh Dan, why are you so awesome?!" with search 
		# string "why are you" goes to 
		# "why are you so awesome?!"
		# Depends on tweet having a .text and .search_string attribute
		# creates a .simpletext attribute
		tweet.text = tweet.text.encode('utf-8', 'ignore')
		tweet.simpletext = phraseify(tweet.text, tweet.search_string)
		return tweet

	def test_search(me):
		results = me.api.GetSearch('"' + me.search_string + '"')
		for r in results:
			print "~~~~~~~~~~~~~~~~~~~~~~"
			r.search_string = search_string
			me.simplify_tweet(r)
			print r.text
			print "="
			print r.simpletext


def main():
	t = TweetDownloader()
	args = sys.argv
	print "=========================="
	print "=========================="
	print "=========================="
	if len(args) == 1:
		t.test_search("why am i")
		print 
		print
		print

		t.test_search("because you")
	else:
		argstr = " ".join(args[1:])
		t.test_search(argstr)

if __name__ == '__main__':
	main()
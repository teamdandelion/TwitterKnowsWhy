#!/usr/bin/env python
import twitter, sys

# Simple Tweet Dictionary:
# 



class TweetDownloader:
	def __init__(me):
		me.api = twitter.Api()

	def simplify_tweet(me, tweet):
		# Uses regular expressions to simplify the tweet to contain
		# a sentance or phrase starting with the search expression
		# eg: "Argh Dan, why are you so awesome?!" with search 
		# string "why are you" goes to 
		# "why are you so awesome?!"
		# Depends on tweet having a .text and .search_string attribute
		# creates a .simpletext attribute
		tweet.simpletext = me.phraseify(tweet.text, tweet.search_string)

	def test_search(me, search_string):
		results = me.api.GetSearch(search_string)
		for r in results:
			print r.text
			print "----------------"


def main():
	t = TweetDownloader()
	args = sys.argv
	print "=========================="
	print "=========================="
	print "=========================="
	if len(args) == 1:
		t.test_search("\"why am i\"")
		print 
		print
		print

		t.test_search("\"because you\"")
	else:
		argstr = " ".join(args[1:])
		t.test_search("\"" + argstr + "\"")

if __name__ == '__main__':
	main()
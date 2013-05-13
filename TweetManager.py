#!/usr/bin/env python
from TweetDownloader import TweetDownloader
from TweetPoster import TweetPoster
import logging
import time, datetime, random

logging.basicConfig(filename='TweetManager.log', level=logging.DEBUG)

class TweetManager(object):
	def __init__(self):
		logging.info("initiating TweetManager")
		why_freshness = 60
		because_freshness = 180
		query_rate = 5
		# logging.debug("freshness={}, query_rate={}".format(freshness, query_rate))
		logging.info("initiating Downloaders")
		self.whyDownloader = TweetDownloader("why am i",
			freshness      = why_freshness,
			query_rate     = query_rate,
			require_match  = True,
			block_retweets = True)

		self.bczDownloader = TweetDownloader("because you",
			freshness      = because_freshness,
			query_rate     = query_rate,
			require_match  = False,
			block_retweets = True)

		self.TweetPoster = TweetPoster()

	def is_good_why(self, t):
		if not self.is_good_tweet(t):
			return False
		return True

	def is_good_bcz(self, t):
		if not self.is_good_tweet(t):
			return False
		return True

	def is_good_tweet(self, t):
		return True			

	def print_with_indices(self, li):
		i = 0
		for l in li:
			print "{} {}".format(i, l)
			i += 1

	def getTweets(self):
		self.whyTweets = self.whyDownloader.GetTweets()
		self.bczTweets = self.bczDownloader.GetTweets()
		self.good_whys = [t for t in self.whyTweets if self.is_good_why(t)]
		self.good_bczs = [t for t in self.bczTweets if self.is_good_bcz(t)]

	def postTweet(self, w, b):
		self.TweetPoster.postTweet(w,b)
		self.whyTweets.remove(w)
		self.bczTweets.remove(b)
		# This removes it from the cache,
		# ensuring that we won't get the same tweet again
		# can throw IOError if combined tweet is too long


	def automate(self):
		self.getTweets()
		if self.good_whys and self.good_bczs:
			w = random.choice(self.good_whys)
			b = random.choice(self.good_bczs)
			self.postTweet(w,b)


	def automateForever(self, period=180):
		while True:
			self.automate()
			time.sleep(period)


	def interact(self):
		print "Operation: You'll be presented with a list of indices."
		print "choose a pair of indices to post, or q to quit, or c "
		print "to continue."
		while True:
			self.getTweets()
			if self.good_whys and self.good_bczs:
				print "======Why Tweets======"
				self.print_with_indices(self.good_whys)
				print "====Because Tweets===="
				self.print_with_indices(self.good_bczs)
				print "======================"

				try: 
					ipt = raw_input("Choose indicies (i,i) or continue: ")
					if ipt == "q": return
					if ipt == "c": continue

					wi, _, bi = ipt.partition(",")
					wi = int(wi)
					bi = int(bi)
					w = self.good_whys[wi]
					b = self.good_bczs[bi]

					print w
					print b
					self.TweetPoster.postTweet(w,b)
					print "==========="

				except ValueError:
					print "Unable to parse input..."
					continue
				except IndexError:
					print "Index out of range."
					continue
				except IOError:
					print "whyTweet would have been too long"
					continue



def main():
	TweetManager().automate()

if __name__ == '__main__':
	main()
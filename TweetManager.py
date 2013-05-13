#!/usr/bin/env python
from TweetDownloader import TweetDownloader
from TweetPoster import TweetPoster
import logging
import time, datetime

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
		return True

	def is_good_bcz(self, t):
		return True

	def print_with_indices(self, li):
		i = 0
		for l in li:
			print "{} {}".format(i, l)
			i += 1

	def automate(self):
		pass


	def interact(self):
		print "Operation: You'll be presented with a list of indices."
		print "choose a pair of indices to post, or q to quit, or c "
		print "to continue."
		while True:
			whyTweets = self.whyDownloader.GetTweets()
			bczTweets = self.bczDownloader.GetTweets()
			good_whys = [t for t in whyTweets if self.is_good_why(t)]
			good_bczs = [t for t in bczTweets if self.is_good_bcz(t)]
			if good_whys and good_bczs:
				print "======Why Tweets======"
				self.print_with_indices(good_whys)
				print "====Because Tweets===="
				self.print_with_indices(good_bczs)
				print "======================"

				try: 
					ipt = raw_input("Choose indicies (i,i) or continue: ")
					if ipt == "q": return
					if ipt == "c": continue

					wi, _, bi = ipt.partition(",")
					wi = int(wi)
					bi = int(bi)
					w = good_whys[wi]
					b = good_bczs[bi]

					print w
					print b
					self.TweetPoster.postTweet(w,b)
					whyTweets.remove(w) # This removes it from the cache,
					# ensuring that we won't get the same tweet again
					bczTweets.remove(b)
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


			# time.sleep(5)

def main():
	TweetManager().interact()

if __name__ == '__main__':
	main()
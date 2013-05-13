#!/usr/bin/env python
from TweetDownloader import TweetDownloader
from TweetPoster import TweetPoster
import logging
import time, datetime, random, argparse
import misc

logging.basicConfig(filename='TweetManager.log', level=logging.DEBUG)

class TweetManager(object):
	def __init__(self, why_freshness, because_freshness):
		logging.info("initiating TweetManager")
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

		self.bad_words    = misc.load_word_set("bad_words.txt")
		# self.bad_whys     = misc.load_word_set("badwhys.txt")
		# self.bad_because  = misc.load_word_set("bads.txt")

	def is_good_tweet(self, t):
		if self.has_bad_words(t, self.bad_words):
			return False
		return True

	def is_good_why(self, t):
		if not self.is_good_tweet(t):
			return False
		# if self.has_bad_words(t, self.bad_whys):
		# 	return False
		return True

	def is_good_bcz(self, t):
		if not self.is_good_tweet(t):
			return False
		# if self.has_bad_words(t, self.bad_bczs):
		# 	return False
		return True

	def has_bad_words(self, t, badset):
		for word in t.phrase.split():
			for substring in misc.get_substrings(word.lower()):
				if substring in badset:
					return True

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
			try:
				w = random.choice(self.good_whys)
				b = random.choice(self.good_bczs)
				print w
				print "(%s)" % w.text
				print "======================"
				print b
				print "(%s)" % b.text
				print "======================"
				self.postTweet(w,b)
			except IOError: # tweet would have been too long
				# let's just try again
				print "Tweet too long! Recovering"
				self.automate()


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
				misc.print_with_indices(self.good_whys)
				print "====Because Tweets===="
				misc.print_with_indices(self.good_bczs)
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
	parser = argparse.ArgumentParser("Tweet Manager")
	# parser.add_argument("-i", "--interactive-mode", dest="i", 
	# 	help="Launch the manager in interactive mode", action="store_true")
	parser.add_argument("-a", "--automate", dest="a",
		help="Launch in automated mode, fires once by default",
		action="store_true")
	parser.add_argument("-r", "--run-forever", dest="r",
		help="Launch in automated mode, activating every (r) seconds",
		action="store", type=int, default=0)
	parser.add_argument("-wf", "--why-freshness", dest="wf",
		help="Set the why-freshness to (wf) default 60",
		type=int, default=60)
	parser.add_argument("-bf", "--because-freshness", dest="bf",
		help="Set the because-freshness to (bf) default 180",
		type=int, default=180)
	args = parser.parse_args()

	TM = TweetManager(why_freshness = args.wf, because_freshness = args.bf)
	if args.r > 0:
		print "Launching automate forever mode with period {}".format(args.r)
		TM.automateForever(args.r)
	elif args.a:
		TM.automate()
	else:
		TM.interact()

if __name__ == '__main__':
	main()
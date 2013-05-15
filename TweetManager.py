#!/usr/bin/env python
from TweetDownloader import TweetDownloader
from TweetPoster import TweetPoster
import logging
import time, datetime, random, argparse
from operator import attrgetter
import misc

logging.basicConfig(filename='TweetManager.log', level=logging.DEBUG)

class TweetManager(object):
	def __init__(self, why_freshness, because_freshness):
		logging.info("initiating TweetManager")
		self.query_rate = 5
		# logging.debug("freshness={}, query_rate={}".format(freshness, query_rate))
		logging.info("initiating Downloaders")
		self.whyDownloader = TweetDownloader("why am i",
			freshness      = why_freshness,
			query_rate     = self.query_rate,
			require_match  = True,
			block_retweets = True)

		self.bczDownloader = TweetDownloader("because you",
			freshness      = because_freshness,
			query_rate     = self.query_rate,
			require_match  = False,
			block_retweets = True)

		self.TweetPoster = TweetPoster()

		self.bad_words    = misc.load_word_set("bad_words.txt")
		self.happy_words  = misc.load_word_set("happy_words.txt")
		# self.bad_whys     = misc.load_word_set("badwhys.txt")
		self.bad_because  = misc.load_word_set("bad_because.txt")

	def is_good_tweet(self, t):
		if self.has_subword(t, self.bad_words):
			return False
		return True

	def is_good_why(self, t):
		if not self.is_good_tweet(t):
			return False
		# if self.has_subword(t, self.bad_whys):
		# 	return False
		return True

	def is_good_bcz(self, t):
		if not self.is_good_tweet(t):
			return False
		if not self.has_subword(t, self.happy_words):
			return False
		if self.has_word(t, self.bad_because):
			return False
		return True

	def has_subword(self, t, wordset):
		for word in t.phrase.split():
			for substring in misc.get_substrings(word.lower()):
				if substring in wordset:
					return True
		return False


	def has_word(self, t, wordset):
		for word in t.phrase.split():
			if word.lower() in wordset:
				return True
		return False

	def getTweets(self):
		self.whyTweets = self.whyDownloader.GetTweets()
		self.bczTweets = self.bczDownloader.GetTweets()
		self.good_whys = [t for t in self.whyTweets if self.is_good_why(t)]
		self.good_bczs = [t for t in self.bczTweets if self.is_good_bcz(t)]

	def postTweet(self, w, b):
		self.whyTweets.remove(w)
		self.bczTweets.remove(b)
		self.TweetPoster.postTweet(w,b)
		# This removes it from the cache,
		# ensuring that we won't get the same tweet again
		# can throw IOError if combined tweet is too long
		# It removes tweets before attempting to post. This is a bit hackish
		# ensures that problematic tweets get thrown out


	def automate(self):
		self.getTweets()
		if self.good_whys and self.good_bczs:
			w = max(self.good_whys, key=attrgetter('created_at_in_seconds'))
			b = max(self.good_bczs, key=attrgetter('created_at_in_seconds'))
			print w
			print "(%s)" % w.text
			print "======================"
			print b
			print "(%s)" % b.text
			print "======================"
			try:
				self.postTweet(w,b)
				return True
			except IOError as e: # tweet would have been too long
				# let's just try again
				print "Tweet too long! Recovering", e
				self.automate()
			except UnicodeDecodeError as e:
				print e
				return False


	def automateForever(self, period=180):
		while True:
			if self.automate():
				time.sleep(period)
			else:
				print "Found nothing. Sleeping to try again"
				time.sleep(self.query_rate)


	def interact(self):
		print "Operation: You'll be presented with a list of indices."
		print "choose a pair of indices to post, or q to quit, or (c)ontinue or (q)uit"
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

				except ValueError as e:
					print "Unable to parse input...", e
					continue
				except IndexError as e:
					print "Index out of range.", e
					continue
				except IOError as e:
					print "whyTweet would have been too long", e
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
		help="Set the because-freshness to (bf) default 5000",
		type=int, default=5000)
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
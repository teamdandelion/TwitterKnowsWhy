from TweetDownloader import TweetDownloader
from TweetPoster import TweetPoster
import logging
import time, datetime, random, argparse
import misc

class TweetListener(object):
	def __init__(self):
		self.TweetPoster = TweetPoster()
		self.MentionDownloader = TweetDownloader("@iknowexactlywhy",
			freshness      = 1000,
			query_rate     = 180,
			block_retweets = True)
		self.tweets_recieved = self.MentionDownloader.GetTweets()
		while self.tweets_recieved:
			self.tweets_recieved.pop()
		# Clears out all old mentions so we don't retweet the same object

	def main(self):
		while True:
			self.MentionDownloader.GetTweets()
			for t in self.tweets_recieved:
				print "Retweeting:", t.text
				self.TweetPoster.postRetweet()
			time.sleep(100) #downloader wont call search more than 1x per 180s


if __name__ == '__main__':
	TweetListener().main()


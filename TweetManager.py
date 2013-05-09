#!/usr/bin/env python
from TweetDownloader import TweetDownloader

import time, datetime, pytz

CST = pytz.timezone("US/Central")

def get_exchanges(nPairs=500):
	why         = TweetDownloader("why am i", require_match=True)
	because     = TweetDownloader("because you", require_match=False)
	whylist     = []
	becauselist = []

	start = time.time()
	whylist     += why._search()
	becauselist += because._search()
	for i in xrange(nPairs):

		if not(whylist and becauselist):
			whylist     += why._search()
			becauselist += because._search()
			time.sleep(4)
			continue

		w = whylist.pop()
		b = becauselist.pop()
		print #"~~~~~~~~~~~~~~~~~~~~~~"
		print w.time.astimezone(CST).strftime("%I:%M:%S%p"),
		print ": ", w.phrase 
		print b.time.astimezone(CST).strftime("%I:%M:%S%p"),
		print ": ", b.phrase 

	end = time.time()

	print "Time elapsed: ", end-start

def call_and_response():
	why         = TweetDownloader("why am i"   , require_match=True )
	because     = TweetDownloader("because you", require_match=False)
	whylist     = []
	becauselist = []

	while True:
		whylist     += why.search()
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

def main():
	get_exchanges(100)

if __name__ == '__main__':
	main()
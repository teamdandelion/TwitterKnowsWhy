import twitter, patch_twitter



class TweetPoster(object):
	"""Takes takes a Why and Because Tweet. Posts to Twitter."""
	def __init__(self):
		with open('twitter_keys.key', 'r') as f:
			keys = f.readlines()
		consumer_key    = keys[0].strip()
		consumer_secret = keys[1].strip()
		access_key      = keys[2].strip()
		access_secret   = keys[3].strip()
		self.api = twitter.Api(consumer_key        = consumer_key, 
							   consumer_secret     = consumer_secret, 
							   access_token_key    = access_key, 
							   access_token_secret = access_secret)

	def postTweet(self, whyTweet, bczTweet):
		whyPhrase = whyTweet.phrase
		bczPhrase = bczTweet.phrase
		whyName = whyTweet.GetUser().GetScreenName()
		bczName = bczTweet.GetUser().GetScreenName()
		text = "@%s: %s (via @%s)" % (whyName, bczPhrase, bczName)
		print text
		if len(text) > 140:
			raise IOError
		self.api.PostRetweet(whyTweet.id)
		self.api.PostUpdate(text)



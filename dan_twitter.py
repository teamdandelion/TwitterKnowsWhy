import twitter
from dateutil.parser import parse as parseTime
from dateutil.tz import tzlocal as localTz

class TwitterError(twitter.TwitterError):
	pass

class Status(twitter.Status):
	def __init__(self, *args):
		twitter.Status.__init__(self, *args)
		self.args = args
		self.time = parseTime(self.created_at)
		self.pretty_time = self.time.astimezone(localTz()).strftime("%I:%M:%S:%p")
		self.phrase = None

	def __str__(self):
		print self.pretty_time + ":",
		print self.phrase or self.text
		

class User(twitter.User):
	pass

class List(twitter.List):
	pass

class DirectMessage(twitter.DirectMessage):
	pass

class Hashtag(twitter.Hashtag):
	pass

class Trend(twitter.Trend):
	pass

class Url(twitter.Url):
	pass

class Api(twitter.Api):
	pass

class _FileCacheError(twitter._FileCacheError):
	pass

class _FileCache(twitter._FileCache):
	pass
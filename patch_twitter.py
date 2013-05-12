import twitter
from dateutil.parser import parse as parseTime
from dateutil.tz import tzlocal as localTz

TwitterStatus = twitter.Status

class Status(TwitterStatus):
	def __init__(self, *args, **kwargs):
		TwitterStatus.__init__(self, *args, **kwargs)
		self.args = args
		self.time = parseTime(self.created_at)
		self.pretty_time = self.time.astimezone(localTz()).strftime("%I:%M:%S:%p")
		self.phrase = None

	def __str__(self):
		return self.pretty_time + ": " + (self.phrase or self.text)
		
twitter.Status = Status
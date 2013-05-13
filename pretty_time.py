import dateutil.tz, time, datetime

local_tz = dateutil.tz.tzlocal()

def prettyDTime(time):
	return time.strftime("%I:%M:%S:%p")

def prettyITime(time):
	dtime = datetime.datetime.fromtimestamp(time, local_tz)
	return prettyDTime(dtime)
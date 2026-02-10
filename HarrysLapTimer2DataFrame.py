def HarrysLapTimer2DataFrame(pathToHarrysLaptimerFile):
  import pandas as pd
	
  COUNT_OF_ROWS_TO_SKIP = 1
	
  df = pd.read_csv(pathToHarrysLaptimerFile, skiprows=COUNT_OF_ROWS_TO_SKIP)
	
	
  return df

def TimeString2Seconds(timeString):
	import datetime
	
	SECONDS_PER_HOUR = 3600
	SECONDS_PER_MINUTE = 60
	MICROSECONDS_PER_SECOND = 1000000
	FORMAT="%M:%S.%f"
	dtObj = datetime.datetime.strptime(timeString, FORMAT)
	
	seconds_hours = dtObj.hour * SECONDS_PER_HOUR
	seconds_minutes = dtObj.minute * SECONDS_PER_MINUTE
	seconds_seconds = dtObj.second
	seconds_microseconds = dtObj.microsecond / MICROSECONDS_PER_SECOND
	seconds = seconds_hours + seconds_minutes + seconds_seconds + seconds_microseconds
	
	return seconds
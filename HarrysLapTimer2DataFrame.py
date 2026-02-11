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


def TIME_LAP2Seconds(dataFrame):
	FIELDNAME_TIMESTRING = "TIME_LAP"
	FIELDNAME_TIMESECONDS = "TIME_LAP_SEC"
	dataFrame[FIELDNAME_TIMESECONDS] = dataFrame[FIELDNAME_TIMESTRING].map(TimeString2Seconds)
	return dataFrame


def LatLongDeg2Rad(dataFrame):
	import math
	RADIANS_SUFFIX = "_RAD"
	FIELDNAME_LATITUDE_DEG = "LATITUDE"
	FIELDNAME_LATITUDE_RAD = FIELDNAME_LATITUDE_DEG + RADIANS_SUFFIX
	FIELDNAME_LONGITUDE_DEG = "LONGITUDE"
	FIELDNAME_LONGITUDE_RAD = FIELDNAME_LONGITUDE_DEG + RADIANS_SUFFIX
	RADIANS_PER_DEGREE = math.pi / 180
	dataFrame[FIELDNAME_LATITUDE_RAD] = dataFrame[FIELDNAME_LATITUDE_DEG] * RADIANS_PER_DEGREE
	dataFrame[FIELDNAME_LONGITUDE_RAD] = dataFrame[FIELDNAME_LONGITUDE_DEG] * RADIANS_PER_DEGREE
	return dataFrame


def HarrysLapTimer2GEMS(pathToHarrysLapTimerFile):
	dataFrame001 = HarrysLapTimer2DataFrame(pathToHarrysLapTimerFile)
	
	dataFrame002 = TIME_LAP2Seconds(dataFrame001)
	
	dataFrame003 = LatLongDeg2Rad(dataFrame002)
	
	dataFrame004 = dataFrame003[["TIME_LAP_SEC","LATITUDE_RAD","LONGITUDE_RAD","SPEED_MPH","HEIGHT_FT","HEADING_DEG","DISTANCE_MILE","LATERALG","LINEALG"]]
	
	return dataFrame004

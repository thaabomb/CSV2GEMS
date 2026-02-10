def HarrysLapTimer2DataFrame(pathToHarrysLaptimerFile):
  import pandas as pd
	
  COUNT_OF_ROWS_TO_SKIP = 1
	
  df = pd.read_csv(pathToHarrysLaptimerFile, skiprows=COUNT_OF_ROWS_TO_SKIP)
	
  for timeString in df['TIME_LAP']:
    time_string_to_deconds(timeString)
	
	 
  return df
	


def time_string_to_seconds(time_string):
	from datetime import datetime, timedelta
	time_obj = datetime.strptime(time_string, "%H:%M:%S")
  seconds = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second).total_seconds()
  return seconds
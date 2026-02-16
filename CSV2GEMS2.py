import pandas
import datetime
import math
import numpy

class CSV2GEMS:
	def __init__(self, countOfLinesToSkip, shouldConvertTime, timeFormat, columnName_Time, shouldRearrangeColumns, shouldConvertLatLong, columnName_Latitude, columnName_Longitude):
		self.countOfLinesToSkip = countOfLinesToSkip
		self.shouldConvertTime = shouldConvertTime
		self.timeFormat = timeFormat
		self.columnName_Time_Original = columnName_Time
		self.shouldRearrangeColumns = shouldRearrangeColumns
		self.shouldConvertLatLong = shouldConvertLatLong
		self.columnName_Latitude = columnName_Latitude
		self.columnName_Longitude = columnName_Longitude
		# Let's make sure we determine the final time column in the constructor so we don't have any issues of state.
		SUFFIX_SECONDS = '_SEC'
		if self.shouldConvertTime:
			self.columnName_Time_Final = self.columnName_Time_Original + SUFFIX_SECONDS
		else:
			self.columnName_Time_Final = self.columnName_Time_Original
	
	def timeString2secs(self, timeString):
		timeObj = datetime.datetime.strptime(timeString, self.timeFormat)
		
		SECONDS_PER_HOUR = 3600
		SECONDS_PER_MINUTE = 60
		MICROSECONDS_PER_SECOND = 1000000
		
		seconds_hours = timeObj.hour * SECONDS_PER_HOUR
		seconds_minutes = timeObj.minute * SECONDS_PER_MINUTE
		seconds_seconds = timeObj.second
		seconds_microseconds = timeObj.microsecond / MICROSECONDS_PER_SECOND
		
		seconds = seconds_hours + seconds_minutes + seconds_seconds + seconds_microseconds
		
		return seconds
	
	def timeColumn2secs(self, dataFrame):
		dataFrame[self.columnName_Time_Final] = dataFrame[self.columnName_Time_Original].map(self.timeString2secs)
		return dataFrame
		
	
	def degColumn2rad(self, dataFrame, columnName_Degrees):
		SUFFIX_RADIANS = "_RAD"
		columnName_Radians = columnName_Degrees + SUFFIX_RADIANS
		RADIANS_PER_DEGREE = math.pi / 180
		dataFrame[columnName_Radians] = RADIANS_PER_DEGREE * dataFrame[columnName_Degrees]
		return dataFrame
	
	def convertCSV(self, pathToCSVFile):
		dataFrame = pandas.read_csv(pathToCSVFile, skiprows=self.countOfLinesToSkip)
		if self.shouldConvertTime:
			dataFrame = self.timeColumn2secs(dataFrame)
		if self.shouldConvertLatLong:
			dataFrame = self.degColumn2rad(dataFrame,self.columnName_Latitude)
			dataFrame = self.degColumn2rad(dataFrame, self.columnName_Longitude)
		if self.shouldRearrangeColumns:
			dataFrame = self.rearrangeColumns(dataFrame)
		return dataFrame
	
	def rearrangeColumns(self, dataFrame):
		columnNames_All = dataFrame.columns
		columnName_Time = self.columnName_Time_Final
		columnNames_Others = numpy.setdiff1d(columnNames_All, columnName_Time)
		columnNames_Time = [columnName_Time]
		# Let's prepend columnName_Time to columnNames_Others'
		columnNames_Rearranged = numpy.array(columnNames_Time + list(columnNames_Others))
		dataFrame = dataFrame[columnNames_Rearranged]
		return dataFrame

HarrysLapTimer = CSV2GEMS(countOfLinesToSkip=1, shouldConvertTime=True, timeFormat="%M:%S.%f", columnName_Time="TIME_LAP", shouldRearrangeColumns=True, shouldConvertLatLong=True, columnName_Latitude="LATITUDE", columnName_Longitude="LONGITUDE")

hltcsv='2025-12-20_Autocross_Run-3-of-6.csv.csv'
hltgems=HarrysLapTimer.convertCSV(hltcsv)
print(hltgems)

ecutek = CSV2GEMS(countOfLinesToSkip=7, shouldConvertTime=False, timeFormat="%S.%f", columnName_Time='Time (s)', shouldRearrangeColumns=True, shouldConvertLatLong=True, columnName_Latitude='GPS Latitude', columnName_Longitude='GPS Longitude')

etcsv='ecutek.csv'
etgems=ecutek.convertCSV(etcsv)
print(etgems)
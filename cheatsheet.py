import math

def MICROMETERS_PER_INCH():
	micrometersPerInch = 25400
	return micrometersPerInch

def INCHES_PER_MICROMETER():
	micrometersPerInch = MICROMETERS_PER_INCH()
	inchesPerMicrometer = 1/micrometersPerInch
	return inchesPerMicrometer

def INCHES_PER_FOOT():
	inchesPerFoot = 12
	return inchesPerFoot

def FEET_PER_INCH():
	inchesPerFoot = INCHES_PER_FOOT()
	feetPerInch = 1/inchesPerFoot
	return feetPerInch

def MICROMETERS_PER_METER():
	micrometersPerMeter = 1000000
	return micrometersPerMeter

def METERS_PER_MICROMETER():
	micrometersPerMeter = MICROMETERS_PER_METER()
	metersPerMicrometer = 1/micrometersPerMeter
	return metersPerMicrometer

def INCHES_PER_METER():
	inchesPerMeter = INCHES_PER_MICROMETER() * MICROMETERS_PER_METER()
	return inchesPerMeter

def METERS_PER_INCH():
	inchesPerMeter = INCHES_PER_METER()
	metersPerInch = 1/inchesPerMeter
	return metersPerInch
	
def FEET_PER_METER():
	inchesPerMeter = INCHES_PER_METER()
	feetPerInch = FEET_PER_INCH()
	feetPerMeter = inchesPerMeter * feetPerInch
	return feetPerMeter

def METERS_PER_FOOT():
	feetPerMeter = FEET_PER_METER()
	metersPerFoot = 1/feetPerMeter
	return metersPerFoot

def FEET_PER_MILE():
	feetPerMile = 5280
	return feetPerMile

def MILES_PER_FOOT():
	feetPerMile = FEET_PER_MILE()
	milesPerFoot = 1/feetPerMile
	return milesPerFoot

def METERS_PER_KILOMETER():
	metersPerKilometer = 1000
	return metersPerKilometer

def KILOMETERS_PER_METER():
	metersPerKilometer = METERS_PER_KILOMETER()
	kilometersPerMeter = 1/metersPerKilometer
	return kilometersPerMeter

def MILES_PER_KILOMETER():
	feetPerMeter = FEET_PER_METER()
	milesPerFoot = MILES_PER_FOOT()
	milesPerMeter = feetPerMeter * milesPerFoot
	metersPerKilometer = METERS_PER_KILOMETER()
	milesPerKilometer = milesPerMeter * metersPerKilometer
	return milesPerKilometer

def KILOMETERS_PER_MILE():
	return 1/MILES_PER_KILOMETER()

def METERS_PER_NAUTICALMILE():
	return 1852

def NAUTICALMILES_PER_METER():
	return 1/METERS_PER_NAUTICALMILE()

def FEET_PER_NAUTICALMILE():
	return METERS_PER_NAUTICALMILE() * FEET_PER_METER()

def NAUTICALMILES_PER_FOOT():
	return 1/FEET_PER_NAUTICALMILE()

def MILES_PER_NAUTICALMILE():
	return FEET_PER_NAUTICALMILE() * MILES_PER_FOOT()

def NAUTICALMILES_PER_MILE():
	return 1/MILES_PER_NAUTICALMILE()


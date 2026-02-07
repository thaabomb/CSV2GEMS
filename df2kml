#!/usr/bin/env python3
“””
Convert a DataFrame with latitude and longitude columns to a KML LineString.
Requires: fastkml, pandas
“””

import pandas as pd
from fastkml import kml
from shapely.geometry import LineString

def dataframe_to_kml_linestring(df, lat_col=‘latitude’, lon_col=‘longitude’,
output_file=‘output.kml’, name=‘Route’,
description=‘Path created from coordinates’):
“””
Convert a pandas DataFrame with latitude and longitude columns to a KML file with a LineString.

```
Parameters:
-----------
df : pandas.DataFrame
    DataFrame containing latitude and longitude data
lat_col : str
    Name of the latitude column (default: 'latitude')
lon_col : str
    Name of the longitude column (default: 'longitude')
output_file : str
    Path to the output KML file (default: 'output.kml')
name : str
    Name for the LineString feature (default: 'Route')
description : str
    Description for the LineString feature (default: 'Path created from coordinates')

Returns:
--------
str : Path to the created KML file
"""

# Validate input
if lat_col not in df.columns or lon_col not in df.columns:
    raise ValueError(f"DataFrame must contain '{lat_col}' and '{lon_col}' columns")

if len(df) < 2:
    raise ValueError("DataFrame must contain at least 2 points to create a LineString")

# Remove any rows with missing values
df_clean = df[[lat_col, lon_col]].dropna()

# Create coordinate pairs (lon, lat) - note KML uses lon, lat order
coordinates = [(row[lon_col], row[lat_col]) for _, row in df_clean.iterrows()]

# Create a Shapely LineString
line = LineString(coordinates)

# Create KML document structure
k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'

# Create a KML Document
doc = kml.Document(ns, 'docid', name, description)
k.append(doc)

# Create a Placemark for the LineString
placemark = kml.Placemark(ns, 'pm1', name, description)
placemark.geometry = line
doc.append(placemark)

# Write to file
with open(output_file, 'w') as f:
    f.write(k.to_string(prettyprint=True))

print(f"KML file created successfully: {output_file}")
print(f"LineString contains {len(coordinates)} points")

return output_file
```

# Example usage

if **name** == “**main**”:
# Create sample data
sample_data = {
‘latitude’: [37.7749, 37.7849, 37.7949, 37.8049],
‘longitude’: [-122.4194, -122.4094, -122.3994, -122.3894],
‘name’: [‘Point A’, ‘Point B’, ‘Point C’, ‘Point D’]
}

```
df = pd.DataFrame(sample_data)

print("Sample DataFrame:")
print(df)
print("\nConverting to KML...")

# Convert to KML
output_path = dataframe_to_kml_linestring(
    df,
    lat_col='latitude',
    lon_col='longitude',
    output_file='route.kml',
    name='Sample Route',
    description='A sample route through San Francisco'
)

print(f"\nKML file saved to: {output_path}")
print("\nYou can open this file in Google Earth or any KML viewer.")
```
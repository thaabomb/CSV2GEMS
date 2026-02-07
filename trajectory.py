#!/usr/bin/env python3
“””
Abstract Data Type for 2D Trajectory with Latitude and Longitude.

This module provides a Trajectory class that represents a sequence of geographic
coordinates and provides methods for trajectory analysis and manipulation.
“””

from typing import List, Tuple, Optional, Iterator
from dataclasses import dataclass
from datetime import datetime
import math
import pandas as pd
from shapely.geometry import LineString, Point
from fastkml import kml

@dataclass
class TrajectoryPoint:
“”“Represents a single point in a trajectory.”””
latitude: float
longitude: float
timestamp: Optional[datetime] = None
altitude: Optional[float] = None
metadata: Optional[dict] = None

```
def __post_init__(self):
    """Validate latitude and longitude ranges."""
    if not -90 <= self.latitude <= 90:
        raise ValueError(f"Latitude must be between -90 and 90, got {self.latitude}")
    if not -180 <= self.longitude <= 180:
        raise ValueError(f"Longitude must be between -180 and 180, got {self.longitude}")

def to_tuple(self) -> Tuple[float, float]:
    """Return (latitude, longitude) tuple."""
    return (self.latitude, self.longitude)

def to_xy(self) -> Tuple[float, float]:
    """Return (longitude, latitude) tuple for geometric operations."""
    return (self.longitude, self.latitude)
```

class Trajectory:
“””
Abstract Data Type for a 2D trajectory.

```
Represents a sequence of geographic coordinates (latitude, longitude) and provides
methods for trajectory analysis, manipulation, and export.
"""

def __init__(self, points: Optional[List[TrajectoryPoint]] = None):
    """
    Initialize a trajectory.
    
    Parameters:
    -----------
    points : List[TrajectoryPoint], optional
        Initial list of trajectory points
    """
    self._points: List[TrajectoryPoint] = points if points is not None else []
    self._validate()

def _validate(self):
    """Validate that all points are TrajectoryPoint instances."""
    for point in self._points:
        if not isinstance(point, TrajectoryPoint):
            raise TypeError("All points must be TrajectoryPoint instances")

# ========== Construction Methods ==========

@classmethod
def from_coordinates(cls, coordinates: List[Tuple[float, float]]) -> 'Trajectory':
    """
    Create trajectory from list of (lat, lon) tuples.
    
    Parameters:
    -----------
    coordinates : List[Tuple[float, float]]
        List of (latitude, longitude) tuples
    
    Returns:
    --------
    Trajectory : New trajectory instance
    """
    points = [TrajectoryPoint(lat, lon) for lat, lon in coordinates]
    return cls(points)

@classmethod
def from_dataframe(cls, df: pd.DataFrame, 
                  lat_col: str = 'latitude',
                  lon_col: str = 'longitude',
                  time_col: Optional[str] = None,
                  alt_col: Optional[str] = None) -> 'Trajectory':
    """
    Create trajectory from pandas DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing coordinate data
    lat_col : str
        Name of latitude column
    lon_col : str
        Name of longitude column
    time_col : str, optional
        Name of timestamp column
    alt_col : str, optional
        Name of altitude column
    
    Returns:
    --------
    Trajectory : New trajectory instance
    """
    points = []
    for _, row in df.iterrows():
        timestamp = row[time_col] if time_col and time_col in df.columns else None
        altitude = row[alt_col] if alt_col and alt_col in df.columns else None
        
        point = TrajectoryPoint(
            latitude=row[lat_col],
            longitude=row[lon_col],
            timestamp=timestamp,
            altitude=altitude
        )
        points.append(point)
    
    return cls(points)

# ========== Basic Operations ==========

def add_point(self, point: TrajectoryPoint) -> None:
    """Add a point to the end of the trajectory."""
    if not isinstance(point, TrajectoryPoint):
        raise TypeError("Point must be a TrajectoryPoint instance")
    self._points.append(point)

def insert_point(self, index: int, point: TrajectoryPoint) -> None:
    """Insert a point at the specified index."""
    if not isinstance(point, TrajectoryPoint):
        raise TypeError("Point must be a TrajectoryPoint instance")
    self._points.insert(index, point)

def remove_point(self, index: int) -> TrajectoryPoint:
    """Remove and return the point at the specified index."""
    return self._points.pop(index)

def clear(self) -> None:
    """Remove all points from the trajectory."""
    self._points.clear()

# ========== Access Methods ==========

def __len__(self) -> int:
    """Return the number of points in the trajectory."""
    return len(self._points)

def __getitem__(self, index: int) -> TrajectoryPoint:
    """Get point at index."""
    return self._points[index]

def __iter__(self) -> Iterator[TrajectoryPoint]:
    """Iterate over trajectory points."""
    return iter(self._points)

def __repr__(self) -> str:
    """String representation of the trajectory."""
    return f"Trajectory({len(self)} points)"

def get_points(self) -> List[TrajectoryPoint]:
    """Return a copy of all points in the trajectory."""
    return self._points.copy()

def get_coordinates(self) -> List[Tuple[float, float]]:
    """Return list of (latitude, longitude) tuples."""
    return [point.to_tuple() for point in self._points]

def get_bounds(self) -> Tuple[float, float, float, float]:
    """
    Get bounding box of trajectory.
    
    Returns:
    --------
    Tuple[float, float, float, float]
        (min_lat, min_lon, max_lat, max_lon)
    """
    if not self._points:
        raise ValueError("Cannot get bounds of empty trajectory")
    
    lats = [p.latitude for p in self._points]
    lons = [p.longitude for p in self._points]
    
    return (min(lats), min(lons), max(lats), max(lons))

def get_center(self) -> Tuple[float, float]:
    """
    Get center point of trajectory bounding box.
    
    Returns:
    --------
    Tuple[float, float]
        (latitude, longitude) of center
    """
    min_lat, min_lon, max_lat, max_lon = self.get_bounds()
    return ((min_lat + max_lat) / 2, (min_lon + max_lon) / 2)

# ========== Geometric Operations ==========

def distance(self, other: 'Trajectory') -> float:
    """
    Calculate Hausdorff distance between this trajectory and another.
    
    Parameters:
    -----------
    other : Trajectory
        Another trajectory to compare with
    
    Returns:
    --------
    float : Hausdorff distance in meters (approximate)
    """
    line1 = LineString([p.to_xy() for p in self._points])
    line2 = LineString([p.to_xy() for p in other._points])
    return line1.hausdorff_distance(line2) * 111320  # Rough conversion to meters

def length(self) -> float:
    """
    Calculate total length of trajectory using Haversine formula.
    
    Returns:
    --------
    float : Total distance in meters
    """
    if len(self._points) < 2:
        return 0.0
    
    total_distance = 0.0
    for i in range(len(self._points) - 1):
        total_distance += self._haversine_distance(
            self._points[i], self._points[i + 1]
        )
    
    return total_distance

def _haversine_distance(self, point1: TrajectoryPoint, 
                       point2: TrajectoryPoint) -> float:
    """
    Calculate distance between two points using Haversine formula.
    
    Returns:
    --------
    float : Distance in meters
    """
    R = 6371000  # Earth's radius in meters
    
    lat1, lon1 = math.radians(point1.latitude), math.radians(point1.longitude)
    lat2, lon2 = math.radians(point2.latitude), math.radians(point2.longitude)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def simplify(self, tolerance: float = 0.0001) -> 'Trajectory':
    """
    Simplify trajectory using Douglas-Peucker algorithm.
    
    Parameters:
    -----------
    tolerance : float
        Simplification tolerance (in degrees)
    
    Returns:
    --------
    Trajectory : Simplified trajectory
    """
    if len(self._points) < 3:
        return Trajectory(self._points.copy())
    
    line = LineString([p.to_xy() for p in self._points])
    simplified_line = line.simplify(tolerance, preserve_topology=True)
    
    simplified_points = []
    for coord in simplified_line.coords:
        lon, lat = coord
        # Find closest original point to preserve metadata
        closest_point = min(self._points, 
                          key=lambda p: (p.latitude - lat)**2 + (p.longitude - lon)**2)
        simplified_points.append(TrajectoryPoint(
            latitude=lat,
            longitude=lon,
            timestamp=closest_point.timestamp,
            altitude=closest_point.altitude
        ))
    
    return Trajectory(simplified_points)

def subsample(self, step: int) -> 'Trajectory':
    """
    Subsample trajectory by taking every nth point.
    
    Parameters:
    -----------
    step : int
        Take every step-th point
    
    Returns:
    --------
    Trajectory : Subsampled trajectory
    """
    return Trajectory(self._points[::step])

def interpolate(self, num_points: int) -> 'Trajectory':
    """
    Interpolate trajectory to have specified number of points.
    
    Parameters:
    -----------
    num_points : int
        Target number of points
    
    Returns:
    --------
    Trajectory : Interpolated trajectory
    """
    if num_points <= len(self._points):
        return self.subsample(len(self._points) // num_points)
    
    line = LineString([p.to_xy() for p in self._points])
    distances = [i / (num_points - 1) for i in range(num_points)]
    
    interpolated_points = []
    for d in distances:
        point_on_line = line.interpolate(d, normalized=True)
        interpolated_points.append(TrajectoryPoint(
            latitude=point_on_line.y,
            longitude=point_on_line.x
        ))
    
    return Trajectory(interpolated_points)

# ========== Analysis Methods ==========

def duration(self) -> Optional[float]:
    """
    Calculate duration of trajectory in seconds.
    
    Returns:
    --------
    float or None : Duration in seconds, or None if no timestamps
    """
    if not self._points or not self._points[0].timestamp:
        return None
    
    timestamps = [p.timestamp for p in self._points if p.timestamp]
    if len(timestamps) < 2:
        return None
    
    return (max(timestamps) - min(timestamps)).total_seconds()

def average_speed(self) -> Optional[float]:
    """
    Calculate average speed in meters per second.
    
    Returns:
    --------
    float or None : Average speed in m/s, or None if no timestamps
    """
    duration = self.duration()
    if duration is None or duration == 0:
        return None
    
    return self.length() / duration

def is_closed(self, threshold: float = 10.0) -> bool:
    """
    Check if trajectory is closed (start and end points are close).
    
    Parameters:
    -----------
    threshold : float
        Distance threshold in meters
    
    Returns:
    --------
    bool : True if trajectory is closed
    """
    if len(self._points) < 3:
        return False
    
    distance = self._haversine_distance(self._points[0], self._points[-1])
    return distance <= threshold

# ========== Export Methods ==========

def to_dataframe(self) -> pd.DataFrame:
    """
    Convert trajectory to pandas DataFrame.
    
    Returns:
    --------
    pd.DataFrame : DataFrame with trajectory data
    """
    data = {
        'latitude': [p.latitude for p in self._points],
        'longitude': [p.longitude for p in self._points],
        'timestamp': [p.timestamp for p in self._points],
        'altitude': [p.altitude for p in self._points]
    }
    return pd.DataFrame(data)

def to_linestring(self) -> LineString:
    """
    Convert trajectory to Shapely LineString.
    
    Returns:
    --------
    LineString : Shapely LineString geometry
    """
    return LineString([p.to_xy() for p in self._points])

def to_kml(self, filename: str, name: str = "Trajectory",
           description: str = "Geographic trajectory") -> str:
    """
    Export trajectory to KML file.
    
    Parameters:
    -----------
    filename : str
        Output KML filename
    name : str
        Name for the trajectory
    description : str
        Description for the trajectory
    
    Returns:
    --------
    str : Path to created KML file
    """
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    
    doc = kml.Document(ns, 'docid', name, description)
    k.append(doc)
    
    placemark = kml.Placemark(ns, 'pm1', name, description)
    placemark.geometry = self.to_linestring()
    doc.append(placemark)
    
    with open(filename, 'w') as f:
        f.write(k.to_string(prettyprint=True))
    
    return filename

def to_geojson(self) -> dict:
    """
    Convert trajectory to GeoJSON format.
    
    Returns:
    --------
    dict : GeoJSON representation
    """
    coordinates = [[p.longitude, p.latitude] for p in self._points]
    
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates
        },
        "properties": {
            "length": self.length(),
            "num_points": len(self),
            "duration": self.duration()
        }
    }
```

# ========== Example Usage ==========

if **name** == “**main**”:
print(”=== Trajectory ADT Example ===\n”)

```
# Create trajectory from coordinates
coords = [
    (37.7749, -122.4194),  # San Francisco
    (37.7849, -122.4094),
    (37.7949, -122.3994),
    (37.8049, -122.3894)
]

traj = Trajectory.from_coordinates(coords)
print(f"Created trajectory with {len(traj)} points")
print(f"Trajectory representation: {traj}")

# Access points
print(f"\nFirst point: {traj[0].to_tuple()}")
print(f"Last point: {traj[-1].to_tuple()}")

# Calculate metrics
print(f"\nTrajectory length: {traj.length():.2f} meters")
print(f"Bounding box: {traj.get_bounds()}")
print(f"Center point: {traj.get_center()}")
print(f"Is closed: {traj.is_closed()}")

# Simplify trajectory
simplified = traj.simplify(tolerance=0.001)
print(f"\nSimplified trajectory: {len(simplified)} points")

# Export to KML
kml_file = traj.to_kml('trajectory_output.kml', 
                       name='San Francisco Route',
                       description='Sample trajectory through SF')
print(f"\nExported to KML: {kml_file}")

# Convert to DataFrame
df = traj.to_dataframe()
print("\nTrajectory as DataFrame:")
print(df)

# Create trajectory from DataFrame
traj2 = Trajectory.from_dataframe(df)
print(f"\nRecreated trajectory from DataFrame: {len(traj2)} points")

print("\n=== Example Complete ===")
```
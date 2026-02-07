#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  6 22:25:56 2026

@author: adam
"""

import pandas

import pandas as pd

df = pd.read_csv('/home/adam/repos/git/thaabomb/autocross-notes/2025-12-20_Autocross_Run-1-of-6.csv', skiprows=1)

allColumns = df.columns

lat = df['LATITUDE']
lon = df['LONGITUDE']

from fastkml import kml
from pygeoif.geometry import LineString
from pathlib import Path

# see https://fastkml.readthedocs.io/en/latest/quickstart.html#build-a-kml-from-scratch


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 23:08:27 2026

@author: adam
"""

import tkinter as tk
from tkinter import filedialog
import csv
import pandas as pd

tkroot = tk.Tk()
tkroot.withdraw()
file_path = filedialog.askopenfilename()

with open(file_path) as csvFile:
    csvLines = csvFile.readlines()

COUNT_OF_LINES_IN_PREVIEW = 10
PREVIEW_RANGE = COUNT_OF_LINES_IN_PREVIEW - 1;
for iLine in range(PREVIEW_RANGE):
    myLine = csvLines[iLine]
    print(str(iLine) + ": " + myLine)

lineNum_FieldsLine = input("Enter the number of the line that contains the Field Names:")

df = pd.read_csv(file_path, skiprows=1)
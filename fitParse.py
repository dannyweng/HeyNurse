import csv
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd
import numpy as np

FIT_DIRECTORY = "Fit/Daily Aggregations/"
# Data Points that might be relevent
# data_keys = 'Distance (m),Average heart rate (bpm),Max heart rate (bpm),Min heart rate (bpm),Average speed (m/s),Step count,Sleep duration (ms),Deep sleeping duration (ms),REM sleeping duration (ms)'.split(',')

# Testing with critical data only
data_keys = 'Distance (m),Average heart rate (bpm),Max heart rate (bpm),Min heart rate (bpm)'.split(',')

fit_data = []
for file in os.listdir(FIT_DIRECTORY)[:-2]:

    date = datetime.strptime(file, '%Y-%m-%d.csv')
    with open(os.path.join(FIT_DIRECTORY, file)) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            time = datetime.strptime(row['Start time'][:5], '%H:%M').time()
            row_datetime = datetime.combine(date, time)
            row_data = {'datetime': row_datetime}

            for key in data_keys:
                if key in row:
                    try:
                        row_data[key] = float(row[key])
                    except ValueError:
                        row_data[key] = None
                else:
                    row_data[key] = None
            fit_data.append(row_data)

df = pd.DataFrame(fit_data)
# print(df)
df.index = df['datetime']
# print(df.index)
df['time'] = pd.to_datetime(df['datetime'], format='%H:%M').dt.time
# print(df['time'])


# Replace all NaN references with 0's
df.fillna(0, inplace=True)
print(df)
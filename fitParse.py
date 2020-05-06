import csv
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd
import numpy as np

FIT_DIRECTORY = "Fit/Daily Aggregations/"
# Data Points that might be relevent
data_keys = 'Distance (m),Average heart rate (bpm),Max heart rate (bpm),Min heart rate (bpm),Average speed (m/s),Step count,Sleep duration (ms),Deep sleeping duration (ms),REM sleeping duration (ms)'.split(',')

# Testing with critical data only
# data_keys = 'Distance (m),Average heart rate (bpm),Max heart rate (bpm),Min heart rate (bpm)'.split(',')

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
# df.index = df['datetime']
# print(df)
# print(df.index)

# Create a time column
# df['time'] = pd.to_datetime(df['datetime'], format='%H:%M').dt.time
# print(df['time'])

# Create a date column
# df['date'] = pd.to_datetime(df['datetime'], format='%d').dt.date
# print(df['date'])

# Replace all NaN references with 0's
df.fillna(0, inplace=True)

# Set datetime as the INDEX otherwise INDEX will be 0,1,2,3,4...
df = df.set_index(['datetime'])
# print(df)

# Use df.loc to query the rows you want
# print(df.loc['2020-04-01'])
# print(df.loc['2020-04-01':'2020-04-02'])
# print(df.loc['2020-04-10 00:00:00': '2020-04-11 00:00:00'])
# print(df.index)
# print(df.columns)
# print(sum(df.at['2020-04-01', 'Average heart rate (bpm)']))
# print(df.at['2020-04-01', 'Average heart rate (bpm)'])
# print(df.at['2020-04-01', 'Average heart rate (bpm)'])
# print(df.count(axis='columns'))



# Two methods to get the MEAN
# countData = df.at['2020-04-01', 'Average heart rate (bpm)']

# num_zeros = (countData == 0).sum()
# num_ones = (countData != 1).sum()
# print(sum(df.at['2020-04-01', 'Average heart rate (bpm)']) / (num_ones+num_zeros))

# print(np.mean(countData))

def googleFitAverage(date, dataType):
    countData = df.at[f'{date}', f'{dataType}']
    # print(np.mean(countData))
    return np.mean(countData)


# print(googleFitAverage('2020-04-01', 'Average heart rate (bpm)'))
# print(googleFitAverage('2020-04-01', 'Distance (m)'))
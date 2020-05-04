#!/usr/bin/env python3

# Google Fit API
# Author: Danny Weng
# Reference:
# https://github.com/dannyweng

# import modules
try:
    ## import argparse for future implementations
    import sys
    import requests
    import time
    import webbrowser
    import config


# Any import errors print to screen and exit
except (Exception, error):
	print ('error')
	sys.exit(1)

'''
ACCESS_TOKEN=""
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  https://www.googleapis.com/fitness/v1/users/me/dataSources
'''

def GoogleFitFunction(resourcePath = 'users/me/dataSources', parameters = ''):
    ACCESS_TOKEN = config.GoogleFitAPI
    #resourcePath = 'users/me/dataSources'
    #parameters = ''

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
    }

    #data = '{"dataStreamName": "FlexibilityMeasure", "type": "raw","application": {"detailsUrl": "http://recoveryapps.com","name": "Stretch Flex","version": "1"},"dataType": {"name": "com.recoveryapps.stretchflex.flexibility","field": [{"name": "ankle_range_degrees","format": "integer"},{"name": "wrist_range_degrees","format": "integer","optional": true}]}}'

    #response = requests.get(f'https://www.googleapis.com/fitness/v1/{resourcePath}{parameters}', headers=headers)
    #response = requests.post(f'https://www.googleapis.com/fitness/v1/{resourcePath}{parameters}', headers=headers)
    #response = requests.post(f'https://www.googleapis.com/fitness/v1/{resourcePath}{parameters}', headers=headers)
    print(response) # Response 200 = OK, 401 = Unauthorized
    print(response.status_code) # Same as above with only the response number
    print(response.text)

    response_json = response.json()

    print(response_json)

# https://developers.google.com/fit/scenarios/read-sleep-data
# https://www.googleapis.com/fitness/v1/users/me/sessions?startTime=2019-12-05T00:00.000Z&endTime=2019-12-17T23:59:59.999Z&activityType=72


# GET
#GoogleFitFunction('users/me/dataSources','/derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm')
#GoogleFitFunction('users/me/dataSources','/derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm')

# POST Need to get permission - Look into Authorization
GoogleFitFunction('users/userId','/dataset:aggregate')



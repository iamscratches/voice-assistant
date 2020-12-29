# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 02:53:33 2020

@author: subhankar
"""
#               get request
from urllib.request import urlopen
import json

READ_API_KEY='BO5WG0XEJ37JQI5C'
CHANNEL_ID='1270994'

NEW_URL = "https://api.thingspeak.com/channels/{}/feeds.json?api_key={}&results=2".format(CHANNEL_ID,READ_API_KEY)
TS = urlopen(NEW_URL)

response = TS.read()

data=json.loads(response.decode('utf-8'))

print(data)

print (data["feeds"][0]["field1"])
print (data["feeds"][0]["field2"])
print (data["feeds"][0]["field3"])
print (data["feeds"][0]["field4"])

print(data["feeds"][1]["field1"])
print(data["feeds"][1]["field2"])
print(data["feeds"][1]["field3"])
print(data["feeds"][1]["field4"])

TS.close()
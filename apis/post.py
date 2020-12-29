# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 03:32:35 2020

@author: subhankar
"""

#                post request
import urllib.request
import time
KEY = "HZ7S7UQH6NFKKO59"
URl='https://api.thingspeak.com/update?api_key=' + KEY + '&field1=0'

HEADER='&field1={}&field2={}&field3={}&field4={}'.format(100,1000,10000,100000)
NEW_URL = URl+KEY+HEADER
print(NEW_URL)
data=urllib.request.urlopen(NEW_URL)
print(data)

# time.sleep(15)

# print("\n")
# HEADER='&field1={}&field2={}&field3={}&field4={}'.format(0,0,0,0)
# NEW_URL = URl+KEY+HEADER
# print(NEW_URL)
# data=urllib.request.urlopen(NEW_URL)
# print(data)
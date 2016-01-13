#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from threading import Thread
import time

baseurl=input("Enter base URL (with http/https): ")
useragent={'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
pathArray=[] #Placeholder for our paths
threadList=[] #Somewhere to put our threads
positives=0 #To keep track of how many matches we get


"""Loads the paths into the pathArray"""
def readLines():
    paths=open("admin_locations.txt", 'r')
    for each in paths:
        pathArray.append(each)
readLines()


def requester(completeURL):
    global positives
    try:
        htmlrequest=requests.get(completeURL, headers=useragent)
    except:
        print("Something failed, overloaded network or something. Missed this request: " + completeURL)
    if positives>5:
        print("Bummer, we are probably getting false positives")
    if htmlrequest.status_code==200:
        print("Found: "+completeURL)
        positives=positives+1


for path in pathArray:
    t=Thread(target=requester,args=(baseurl+path,))
    t.start()
    time.sleep(.1) #We can be somewhat gentle :)
    threadList.append(t)


for tlist in threadList:
    t.join()



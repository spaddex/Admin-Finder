#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

baseurl=input("Enter base URL (with http/https): ")
useragent={'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

def readLines():
    paths=open("admin_locations.txt", 'r')
    while len(str(paths))>0:
        for each in paths:
            checkURL(each)

def checkURL(path):
    completeURL=baseurl+path
    print(completeURL)
    grab=requests.get(completeURL, headers=useragent)
    print(grab.status_code) #Comment if you only want the found URLS to be printed
    if grab.status_code==400:
        print("Found: "+  completeURL)

readLines()
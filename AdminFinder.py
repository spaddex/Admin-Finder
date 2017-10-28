#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import sys
import time
import re
import requests
from threading import Thread

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



useragent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
pathArray = []  # Placeholder for our paths
threadList = []  # Somewhere to put our threads
positives = 0  # To keep track of how many matches we get
foundPages = []
inform = 0
baseURLLenght = 0

#Loads the paths into the pathArray
def readLines():
    with open("admin_locations.txt", 'r') as x:
        paths = x.readlines()
        for path in paths:
            pathArray.append(str(path))
        print("Loaded " + str(len(pathArray)) + " paths")


# Sends the requests, and prints if URL is found
def requester(completeURL):
    global positives, htmlrequest, inform
    try:
        htmlrequest = requests.get(completeURL, headers=useragent, allow_redirects=False)
        showRequest(htmlrequest)
        #print(completeURL)
        if htmlrequest.status_code == 200:
            positives += 1
            foundPages.append(completeURL)
    except Exception as exp:
        print(bcolors.WARNING + "Something failed: " + str(exp) + ". Missed this request: " + str(completeURL) + bcolors.ENDC)
    if positives < 5 and (htmlrequest.status_code == 200):
        print(bcolors.OKGREEN + "Found: " + str(completeURL) + bcolors.ENDC)
    elif positives > 5 and (inform == 0):
        print(bcolors.FAIL + "Never mind, false positives. Send me a ctrl+c" + bcolors.ENDC)
        inform += 1


# Indents and prints requests
def showRequest(requestObject):
    global baseURLLenght
    allLenghts = [len(x) for x in pathArray]
    longestRequest = (int(baseURLLenght) + int(max(allLenghts)))
    indentLenght = (longestRequest + 3) - len(requestObject.url)
    print(str(requestObject.url) + indentLenght*' '  + 'status code: ' + str(requestObject.status_code) + '\t response size: ' + str(len(requestObject.content)))


# Get input on commandline
def getAttackURL():
    if len(sys.argv) == 2:  # Check if we got input on commandline
        target = str(sys.argv[1])
        if(target.startswith('http')) == False:  # Check if schema was supplied
            print(bcolors.WARNING + "HTTP / HTTPS not specified, assuming HTTP" + bcolors.ENDC)
            target = ('http://'+str(target))
        if(target[-1:]) == '/':  # if last char is / (http://example.com/)
            return(target[:-1])  # return URL minus last char (http://example.com)
        else:
            return target
    else:
        target = askForAttackURL()  # fall over to asking for input
        return target


# Will ask the user for input instead
def askForAttackURL():
    target = input("Enter base URL (with http/https): ")
    if (target.startswith('http')) == False:
        print(bcolors.WARNING + "HTTP / HTTPS not specified, assuming HTTP" + bcolors.ENDC)
        target = ('http://' + str(target))
    if (target[-1:]) == '/':  # if last char is / (http://example.com/)
        return (target[:-1])  # return URL minus last char (http://example.com)
    else:
        return target


def main():
    global baseURLLenght
    baseurl = getAttackURL()
    baseURLLenght = len(baseurl)
    readLines()
    try:
        for path in pathArray:
            t = Thread(target=requester, args=(baseurl + path.strip(),))
            t.start()
            time.sleep(.1)  # We can be somewhat gentle :)
            threadList.append(t)
        for tlist in threadList:
            t.join()
    except KeyboardInterrupt:
        print(bcolors.HEADER + "Shutting Down" + bcolors.ENDC)
    except TypeError:
        print(bcolors.FAIL + "Did you input an URL?" + bcolors.ENDC)
        print(("Details: \n {} \n {} Line: {} \n" + bcolors.ENDC).format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
        return 0

    if positives == 0:
        print(bcolors.FAIL + "Couldn't find any admin-page" + bcolors.ENDC)
    elif positives > 6:
        print(bcolors.WARNING + "Many hits, probably false positives" + bcolors.ENDC)
        for page in foundPages:
            print(str(page))
    elif positives < 6:
        print(bcolors.OKBLUE + " Found pages: " + bcolors.ENDC)
        for page in foundPages:
            print("  " + str(page.strip()))


if __name__ == "__main__":
    main()

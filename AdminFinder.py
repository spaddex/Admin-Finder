#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import requests
from threading import Thread
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

baseurl = input("Enter base URL (with http/https): ")
useragent = {
	'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
pathArray = []  # Placeholder for our paths
threadList = []  # Somewhere to put our threads
positives = 0  # To keep track of how many matches we get
foundPages = []
inform=0

"""Loads the paths into the pathArray"""
def readLines():
	with open("admin_locations.txt", 'r') as x:
		paths=x.readlines()
		for path in paths:
			pathArray.append(str(path))
		print("Loaded " + str(len(pathArray)) + " paths")



def requester(completeURL):
	global positives, htmlrequest, inform
	try:
		htmlrequest = requests.get(completeURL, headers=useragent, allow_redirects=False)
		print(completeURL)
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



def main():
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
		print( bcolors.HEADER + "Shutting Down" + bcolors.ENDC)

	if positives == 0:
		print(bcolors.FAIL + "Couldn't find any admin-page" + bcolors.ENDC)
	elif positives > 6:
		print(bcolors.WARNING + "Many hits, probably false positives" + bcolors.ENDC)
		for page in foundPages:
			print(str(page))
	elif positives < 6:
		print(bcolors.OKBLUE+ " Found pages: ")
		for page in foundPages:
			print("  " + str(page.strip()))

if __name__ == "__main__":
	main()

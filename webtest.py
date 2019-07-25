#Author: Eric Croiset
#Date: 26.07.2019
#Imports
import requests
import sys
import sched, time
import re
from urllib.parse import urlparse

#Functions for checking HTTP(websitecheck) and HTTPS (websitecheckS) Response Codes
def websitecheck(sc):
	try:
		r = requests.head(checkurl)
		code = r.status_code
	except requests.ConnectionError:
		print("Failed to connect!")
	if (code == 200):
		print("\033[1;32;40m [HTTP PASS] " + "\033[1;37;40m  Code: " + str(code) + " Good HTTP Response")
	elif ( code == 301):
		print("\033[1;32;40m [HTTP PASS] " + "\033[1;37;40m  Code: " + str(code) + " Good HTTP Redirect")
	else:
		print("\033[1;31;40m [HTTP FAIL] " + "\033[1;37;40m Something's wrong! Check the HTTP status code: " + str(code))
	s.enter(tloop, 1, websitecheck, (sc,))

def websitecheckS(sc):
	try:
		r = requests.head(checkurlS)
		codeS = r.status_code
	except requests.ConnectionError:
		print("Failed to connect!")
	if (codeS == 200):
		print("\033[1;32;40m [HTTPS PASS] " + "\033[1;37;40m Code: " + str(codeS) + " Good HTTPS Response")
	else:
		print("\033[1;31;40m [HTTPS FAIL] " + "\033[1;37;40m Something's wrong! Check the HTTPS status code: " + str(codeS))
	s.enter(tloop, 1, websitecheckS, (sc,))

#Definitions
regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

tstart=1 #Time to wait until first check
tloop=5 #Time to wait between checks
s = sched.scheduler(time.time, time.sleep) #Initializing scheduler
b = sched.scheduler(time.time, time.sleep)
startcheck = s.enter(tstart, 1, websitecheck, (s,)) #Defining Timer for HTTP check
startcheckS = s.enter(tstart, 1, websitecheckS, (s,)) #defining timer for https check
domain = sys.argv[1] #Taking argument from commandline and saving it


#For Url Manipulation urllib.parse was used and urlparse does not work with domains without protocol.
#This prepares the variable that will be given to "websitecheck" and "websitecheckS"
if ("http" in domain):
	url = urlparse(domain)
	checkurl = "http://" + url.hostname
	checkurlS = "https://" + url.hostname

else:
	url = domain
	checkurl = "http://" + url
	checkurlS = "https://" + url
#If the Domain matches the regex the user will be asked if he wants to check http or https or both.
if (re.match(regex, checkurl) is not None):
	print("This script will request the status code every " + str(tloop) + " seconds.")
	d1a =  input("Do you want to: A) check for HTTP and HTTPS simultaniously. B) check for HTTP. C) check for HTTPS. [A/B/C]! : ")
	if (d1a == "A"):
		startcheck
		startcheckS
	elif (d1a == "B"):
		startcheck
	elif (d1a == "C"):
		startcheckS
	s.run()
	b.run()
#If the domain does not match the user will be asked to correct it.
if (re.match(regex, checkurl) is None):
	print("The FQDN you entered does not seem to match the regular expression.")
	print("Please make sure the domain you give as argument to this script looks like these examples:")
	print("https://example.com | http://example.com | https://example.com:[Portnumber] | http://example:com[portnumber]")
	quit()

#Instructions for the script
if (domain == "help"):
	print("Usage: python3 webtest.py [Domain]")
	print("HTTP-Info: HTTP-Code 301 redirect will be counted as a successfull connection!")
	print("Port not needed")
	quit()

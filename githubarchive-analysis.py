# -*- coding: utf-8 -*-
#
# Load Organization events from GitHub Archive files
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: GPL v.3
#
# Requisite: 
# install pyGithub with pip install PyGithub
# install Chardet with pip install chardet
#
# PyGitHub documentation can be found here: 
# https://github.com/jacquev6/PyGithub
#

from github import Github
import json
import gzip
import getpass
import glob
import os
import urllib
from datetime import date, datetime
from dateutil.rrule import rrule, DAILY, HOURLY
#import chardet
import codecs
import ijson

users = {}
members = {}
events = {}

print ""
print "Load Organization events from GitHub Archive files"
print ""

userlogin = raw_input("Login: Enter your username: ")
password = getpass.getpass("Login: Enter yor password: ")
username = raw_input("Enter the username you want to analyse: ")
print ""
g = Github( userlogin, password )

print "ORGANIZATIONS:"
for i in g.get_user(username).get_orgs():
	print "-", i.login
print ""

org_to_mine = raw_input("Enter the name of the Organization you want to analyse: ")
print ""

directory = org_to_mine+"-stats"
if not os.path.exists(directory):
	os.makedirs(directory)
	
directory2 = directory+"/"+"githubarchive"
if not os.path.exists(directory2):
	os.makedirs(directory2)

org = g.get_organization(org_to_mine)
	
print org.login,"has",org.public_repos, "repositories."

print ""
for repo in org.get_repos():
	print "-",repo.name
print "" 

for en,user in enumerate(org.get_members()):
	pass

print org.login,"has",en, "members."

for k,user in enumerate(org.get_members()):
	print "-", user.login
	members[user.login] = k

# Members: only the people added to the organization
# Users: people added to the organization plus followers and watchers

# Get all users in the organization by each repository
# Get all the roles for each user
print ""
print ".........................................................................."
print ""
print "Analyzing users..."
print ""
for repo in org.get_repos():
	print ""
	print "---------"
	print "NOW ANALYSING:", repo.name
	repository = org.get_repo(repo.name)

	print ""
	print "WATCHERS:",repository.watchers
	print ""
	for i in repository.get_stargazers():
		if i != None:
			print "-",i.login
			if i.login not in users:
				users[i.login] = {}
				users[i.login]["watcher"]="Yes"
			else:
				users[i.login]["watcher"]="Yes" 
		else:
			users["None"]["watcher"]="Yes" 
	print ""
	print "COLLABORATORS"
	print ""
	for i in repository.get_collaborators():
		if i != None:
			print "-",i.login
			if i.login not in users:
				users[i.login] = {}
				users[i.login]["collaborator"]="Yes"
			else:
				users[i.login]["collaborator"]="Yes"
		else:
			users["None"]["collaborator"]="Yes"
	print ""
	print "CONTRIBUTORS"
	print ""
	for i in repository.get_contributors():
		if i.login != None:
			print "-", i.login
			if i.login not in users:
					users[i.login] = {}
					users[i.login]["contributor"]="Yes"
			else:
				users[i.login]["contributor"]="Yes"
		else:
			users["None"]["contributor"]="Yes"
			
	# Check the attributes of every node, and add a "No" when it is not present
	for i in users:
		if "owner" not in users[i]:
			users[i]["owner"] = "No"
		if "contributor" not in users[i]:
			users[i]["contributor"] = "No"               
		if "collaborator" not in users[i]:
			users[i]["collaborator"] = "No"
		if "watcher" not in users[i]:
			users[i]["watcher"] = "No"

print ""
print ""
choice = raw_input("Do you want to download archives of past events or do you have alredy them and want to load them? (download / load) ")
print ""

if choice == "download" or choice == "Download" or choice == "DOWNLOAD":
	# Saving files from githubarchive.org
	# http://www.githubarchive.org/
	# More options here: http://python.dzone.com/articles/how-download-file-python

	print ""
	print ".........................................................................."
	print ""
	print "Downloading files..."
	print ""
	print "This program will now download all the archives of the GitHub events."
	print "Be sure to have enough space on your hard drive."
	print ""

	first = str(raw_input("Starting date (year/month/day): "))
	try:
		start = datetime.strptime(first, '%Y/%m/%d')
	except ValueError:
		print "Incorrect date format."
		exit()
	second = str(raw_input("Ending date (year/month/day): "))
	try:
		end = datetime.strptime(second, '%Y/%m/%d')
	except ValueError:
		print "Incorrect date format."
		exit()

	print ""
	for day in rrule(DAILY, dtstart=start, until=end):
		now = day.strftime("%Y-%m-%d")
		for hour in range(1,24):
			hour_string = str(hour) 
			filename = now+"-"+hour_string+".json.gz"
			url = "http://data.githubarchive.org/" + filename
			print "Downloading",url
			#urllib.urlretrieve(url, filename)
			urllib.urlretrieve(url, directory2+"/"+filename)
		
	print ""
	print "All files downloaded."
	print ""

print ".........................................................................."
print ""
print "Loading files..."
print ""

os.chdir(directory2)
allfiles = glob.glob('./*.json.gz')
print "Analyzing",len(allfiles),"files..."

for i in users:
	events[i]={}

errors = 0

for currentfile in allfiles:
	print ""
	print "Loading",currentfile
	
	# OK
	#f = gzip.open(currentfile)
	#reader = codecs.getreader("utf-8")
	#data = reader(f)
	
	
	#fp = gzip.open(currentfile)
	#contents = fp.read()
	#fp.close()
	#data = json.loads(contents, 'utf-8')
	
	with gzip.open(currentfile) as f:
		try:
	  		lines = f.read().splitlines()
			for line in lines:
				data = json.loads( '['+ unicode(line, errors='replace').replace('}{', '},{')+']' )
				for i in range(len(data)):
				  rec = data[i]
			  
				  if "repository" in rec:
					if "organization" in rec["repository"]:
						if rec["actor"] in users and rec["repository"]["organization"] == org.login:
							print "Event found.....by",rec["actor"],"with",rec["type"],"within",rec["repository"]["name"],"at",rec["created_at"]
							events[rec["actor"]][k] = {}
							time = datetime.strptime(rec["created_at"][:-6], "%Y-%m-%dT%H:%M:%S")
							events[rec["actor"]][k]["time"] = time
							events[rec["actor"]][k]["type"] = rec["type"]
							events[rec["actor"]][k]["repo"] = rec["repository"]["name"]
		except:
			print ""
			print "There was an error decoding the event:",line
			errors += 1
				
print ".........................................................................."
print ""
print "Events collected..."
print ""
for i in events:
	for k in events[i]:
		events[i][k]["time"] = str(events[i][k]["time"])
print json.dumps(events, sort_keys=True, indent=4)

print ".........................................................................."
print ""
print "Saving file..."
print ""

# Save content as json file
os.chdir('..')
with open("events.json", 'w') as outfile:
	json.dump(events, outfile)
	
print "Done.", errors, "conversion errors. Please check that they did not affect the data you were looking for."
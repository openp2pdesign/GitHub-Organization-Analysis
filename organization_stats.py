# -*- coding: utf-8 -*-
#
# General statistics of an Organization repository in GitHub
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: GPL v.3
#
# Requisite: 
# install pyGithub with pip install PyGithub
# install Matplotlib with pip install matplotlib
#
# PyGitHub documentation can be found here: 
# https://github.com/jacquev6/PyGithub
#

from github import Github
import getpass

import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import operator

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

users = {}
events = {}

if __name__ == "__main__":
    print "Simple statistics of your GitHub Organization"
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
    
    org = g.get_organization(org_to_mine)
    
    # Create a directory with the name of the organization for saving analysis
    directory = org_to_mine+"-stats"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    print org.login,"has",org.public_repos, "repositories."
    
    print ""
    
    for repo in org.get_repos():
        print "-",repo.name
    
    print ""    
    
    # Get all users in the organization by each repository
    # Get all the roles for each user
    for repo in org.get_repos():
        print "---------"
        print "NOW ANALYSING:", repo.name
        repository = org.get_repo(repo.name)

        print "-----"
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
        print "-----"
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
        print "-----"
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

        
    # Get all events in the organization
    # Description: http://developer.github.com/v3/activity/events/types/
    for j in org.get_events():
        print "-- ",j.type,"event by",j.actor.login,"from repo:",j.repo.name
        if j.actor.login not in events:
            events[j.actor.login] = {}        
        events[j.actor.login][j.id] = {}
        events[j.actor.login][j.id]["time"] = j.created_at
        events[j.actor.login][j.id]["type"] = j.type
        events[j.actor.login][j.id]["repo"] = j.repo.name
    
    # Debug
    print events
    
    # ................................................................................................
    # Separate activities by repository ..............................................................
    # Push, Issue, IssueComment, CommitComment, Fork, Pull
    
    # ................................................................................................
    # Separate activities by person ..................................................................
    # Push, Issue, IssueComment, CommitComment, Fork, Pull
    
    data = {}
    for singleuser in events:
        data[singleuser] = {}
        data[singleuser]["push"] = 0
        data[singleuser]["issue"] = 0
        data[singleuser]["fork"] = 0
        data[singleuser]["commit"] = 0
        data[singleuser]["branchtag"] = 0
        for j in events[singleuser]:
            # Count by event types
            # List of event types: http://developer.github.com/v3/activity/events/types/          
            # print "TYPE:",events[singleuser][j]["type"]
            tipo = events[singleuser][j]["type"]
            if tipo == "PushEvent":
                data[singleuser]["push"] += 1
            elif tipo == "IssuesEvent" or tipo == "IssueCommentEvent":
                data[singleuser]["issue"] += 1
            elif tipo == "ForkEvent" or tipo == "PullRequestEvent" or tipo == "PullRequestReviewCommentEvent":
                data[singleuser]["fork"] += 1
            elif tipo == "CommitCommentEvent":
                data[singleuser]["commit"] += 1
            elif tipo == "CreateEvent" or tipo == "DeleteEvent":
                data[singleuser]["branchtag"] += 1
            else:
                pass
            
    # Transform the dictionary into lists of data
    pushcount = []
    issuecount = []
    forkcount = []
    commitcount = []
    branchtagcount = []
    for singleuser in events:
        pushcount.append(data[singleuser]["push"])
        issuecount.append(data[singleuser]["issue"])
        forkcount.append(data[singleuser]["fork"])
        commitcount.append(data[singleuser]["commit"])
        branchtagcount.append(data[singleuser]["branchtag"])
    
    print "PUSH values:",pushcount
    print "ISSUES values:",issuecount
    print len(pushcount)
    
    # Example from http://matplotlib.org/examples/api/barchart_demo.html
    N = len(events)
    allusers = events.keys()
    
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, pushcount, width, color='r')
    rects2 = ax.bar(ind+width, issuecount, width, color='y')
    
    # add some
    ax.set_ylabel('Activity')
    ax.set_xlabel('Users')
    ax.set_title('Activity by user')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(allusers)
    plt.gcf().autofmt_xdate()
    
    ax.legend( (rects1[0], rects2[0]), ('Push', 'Issues') )
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    # Set picture size
    # fig = plt.gcf()
    # fig.set_size_inches(20,10.5)
    
    # Save plot
    plt.savefig(directory+"/"+"Activities-by-person.png",dpi=200)
    plt.savefig(directory+"/"+"Activities-by-person.pdf")
    plt.show()
    exit()

    
    
    # ................................................................................................
    # All activity through time, by person ...........................................................
    
    # Get the highest level of activities, for y scale
    activities = []
    for singleuser in events:
        days = {}
        for j in events[singleuser]:
            # Define activities per day
            day = datetime.date(events[singleuser][j]["time"].year, events[singleuser][j]["time"].month, events[singleuser][j]["time"].day)
            if day not in days:
                days[day] = {}
                days[day]["activity"] = 0
            days[day]["activity"] = days[day]["activity"] + 1
        print singleuser," - HIGHEST DAY ACTIVITY:", max(days.iteritems(), key=operator.itemgetter(1))[1]["activity"]
        print singleuser," - WHEN:", max(days.iteritems(), key=operator.itemgetter(1))[0]
        activities.append(max(days.iteritems(), key=operator.itemgetter(1))[1]["activity"]) 
    max_activity = max(activities)
    
    # Calculate and draw and save a plot for each user
    for singleuser in events:
        print "--------------------"
        print "USER:",singleuser
        print "TOTAL ACTIVITY:", len(events[singleuser]), "events."
        days = {}
        for j in events[singleuser]:
            #print "TYPE:",events[singleuser][j]["type"]
            # Define activities per day
            day = datetime.date(events[singleuser][j]["time"].year, events[singleuser][j]["time"].month, events[singleuser][j]["time"].day)
            if day not in days:
                days[day] = {}
                days[day]["activity"] = 0
            days[day]["activity"] = days[day]["activity"] + 1
        
        # Sort the dictionary
        ordered = OrderedDict(sorted(days.items(), key=lambda t: t[0]))
        
        # Transform the dictionary in x,y lists for plotting
        x = []
        y = []
        for k,l in enumerate(ordered):
            x.append(l)
            y.append(ordered[l]["activity"])
        
        # Plot a bar
        plt.bar(x, y)
        
        # Plot a line
        #plt.plot_date(x, y, linestyle="dashed", marker="o", color="green")
        
        # Configure plot
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Single activities")
        plt.title("Activity by "+singleuser)
        # Edit the following line if you want to specify manually the time range
        #plt.xlim([datetime.date(2013,11,1), datetime.date(2014,1,9)])
        # The following line does automatic time range according to the life of the organization
        plt.xlim(org.created_at,org.updated_at)
        plt.ylim(0,max_activity)
        
        # Set picture size
        # fig = plt.gcf()
        # fig.set_size_inches(20,10.5)
        
        # Save plot
        plt.savefig(directory+"/"+singleuser+"-timeline.png",dpi=200)
        plt.savefig(directory+"/"+singleuser+"-timeline.pdf")
        plt.show()
    
    # ................................................................................................
    # All activity trough time, all persons...........................................................
    
    print "Done."
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
    
    print org.login,"has",org.public_repos, "repositories."
    
    print ""
    
    for repo in org.get_repos():
        print "-",repo.name
    
    print ""    
    
    # Get all users in the organization by each repository
    # Get all the roles for each user
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

        
    # Get all events in the organization
    # Description: http://developer.github.com/v3/activity/events/types/
    for j in org.get_events():
        print "-- ",j.type,"event by",j.actor.login,"from repo:",j.repo.name
        if j.actor.login not in events:
            events[j.actor.login] = {}        
        events[j.actor.login][j.id] = {}
        events[j.actor.login][j.id]["time"] = j.created_at
        events[j.actor.login][j.id]["type"] = j.type
        events[j.actor.login][j.id]["repo"] = j.repo.name
    
    print events
    
    print "Done. Saved as "+username+"_allrepositories_social_interactions_analysis.gexf"
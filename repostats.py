# -*- coding: utf-8 -*-

from github import Github

issue = {}
issue = {0:{"author":"none", "comments":{}}}
commits = {0:{"commit","sha"}}
repos = {}
users = {}
events = {}

def analyse_repo(repository,organization):  
    
    # Get all events in the organization
    # Description: http://developer.github.com/v3/activity/events/types/
    for j in organization.get_events():
        print "-- event by",j.actor.login
        print "REPO",j.repo.name
        if j.actor.login not in events:
            events[j.actor.login] = {}        
        events[j.actor.login][j.id] = {}
        events[j.actor.login][j.id]["time"] = j.created_at
        events[j.actor.login][j.id]["type"] = j.type
        events[j.actor.login][j.id]["repo"] = j.repo.name
        
        if j.type == "IssuesEvent":
            pass
        elif j.type == "CommitCommentEvent":
            pass
        elif j.type == "PushEvent":
            pass
        elif j.type == "DeleteEvent":
            pass
        elif j.type == "CreateEvent":
            pass
        elif j.type == "IssueCommentEvent":
            pass
        elif j.type == "":
            pass
        elif j.type == "":
            pass
        elif j.type == "":
            pass
        elif j.type == "":
            pass
        elif j.type == "":
            pass
    
    print "EVENTS:"
    print events
    
    print "-----"
    print "DESCRIPTION:",repository.description
    print "-----"
    print "OWNER:",repository.owner.login
    print str(unicode(repository.owner.login)), "owner=yes"
    
    # Add users --------------------------------------------------------------------------
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
    
    # Add empty dictionaries for users' activities
    for i in users:
        users[i]["issues"] = {}
        users[i]["comments"] = {}
        users[i]["commits"] = {}
        
    for i in users:
        print i
        print i.get_events()
    
    # Add users' activities --------------------------------------------------------------------------    
    print "-----"
    print "HAS ISSUES=",repository.has_issues
    if repository.has_issues == True:
        print "-----"
        print "ISSUES: Open ones"
        print ""
        for i in repository.get_issues(state="open"):
            print "Issue number:",i.number
            if i.user != None:
                print "- Created by", i.user.login
                users[i.user.login]["issues"][i.number]= {}
                users[i.user.login]["issues"]["created_at"]= i.created_at
            else:
                print "- Created by None"
                users["None"]["issues"][i.number]= {}
                users["None"]["issues"]["created_at"]= i.created_at
            print "--",i.comments,"comments"
            for j,f in enumerate(i.get_comments()):
                if f.user != None:
                    print "--- With a comment by",f.user.login                    
                    users[f.user.login]["comments"][j]["created_at"]= f.created_at           
                else:
                    print "--- With a comment by None"
                    users["None"]["comments"][j]["created_at"]= f.created_at
            print ""      

        print "ISSUES: Closed ones"
        print ""
        for i in repository.get_issues(state="closed"):
            print "Issue number:",i.number
            if i.user != None:
                print "- Created by", i.user.login
                users[i.user.login]["issues"][i.number]= {}
                users[i.user.login]["issues"]["created_at"]= i.created_at
            else:
                print "- Created by None"
                users["None"]["issues"][i.number]= {}
                users["None"]["issues"]["created_at"]= i.created_at

            print "--",i.comments,"comments"
            for j,f in enumerate(i.get_comments()):
                if f.user != None:
                    print "--- With a comment by",f.user.login
                    users[f.user.login]["comments"][j]["created_at"]= f.created_at 
                else:
                    print "--- With a comment by None"
                    users["None"]["comments"][j]["created_at"]= f.created_at 
            print ""      
              
    
    print "-----"
    print "COMMITS"
    print ""
    
    for k,i in enumerate(repository.get_commits()):
        print "-",i.sha
        if i.committer != None:
            print "-- by",i.committer.login
            print "STATUS:", i.get_statuses() 
            for b in i.get_statuses():
                print "L:",b
                print "date:", b.created_at
            #users[i.committer.login]["commits"][j]["created_at"]= i.author["date"] 
        else:
            print "-- by None"
    print "-----"
       
      
    # Creating the edges from the commits and their comments.
    # Each comment interacts with the previous ones,
    # so each user interacts with the previous ones that have been creating the issue or commented it
    print ""
    print "-----"
    print "ADDING EDGES FROM COMMENTS IN COMMITS"
    print ""
    
    comm = {}
    
    for k,i in enumerate(repository.get_commits()):
        if i.author != None:
            print "Commit by: ",i.author.login
        comm[k]= {}
        comm[k]["comments"]= {}
        
        for m,f in enumerate(i.get_comments()):
            print "- Commented by: ",f.user.login
            comm[k]["comments"][m] = f.user.login
            graph.add_edge(str(f.user.login),str(i.author.login))
            print "- Adding an edge from ",f.user.login, "to", i.author.login
    
            for l in range(m):
                print "- Adding an edge from ",f.user.login,"to",comm[k]["comments"][l]
                graph.add_edge(str(f.user.login),str(comm[k]["comments"][l]))
    
    print "-----"
       
    
    
    # Creating the edges from the issues and their comments.
    # Each comment interacts with the previous ones,
    # so each user interacts with the previous ones that have been creating the issue or commented it
    print ""
    print "-----"
    print "ADDING EDGES FROM ISSUES COMMENTING"
    print ""
    
    for a,b in enumerate(issue):
        print "-----"
        print "Issue author:",issue[a]["author"]
        print ""
        for k,j in enumerate(issue[a]["comments"]):
            print "Comment author:",issue[a]["comments"][k]
            print "Adding an edge from:",issue[a]["comments"][k],"to:",issue[a]["author"]
            graph.add_edge(str(issue[a]["comments"][k]),str(issue[a]["author"]))

            for l in range(k):
                print "Adding an edge from:",issue[a]["comments"][k],"to:",issue[a]["comments"][l]
                graph.add_edge(str(issue[a]["comments"][l]),str(issue[a]["comments"][l]))
    print ""
    
    
    #print "FORKS"
    #print ""
    #for f,i in enumerate(repository.get_forks()):
    #    print i.name
    #    print "ANALYSING A FORK, number",f
    #    print ""
    #    analyse_repo(i,f+1)
    #    print ""
    #print "-----"
    
    print "-----"
    print "PULL REQUESTS"
    print ""
    
    for i in repository.get_pulls():
        print i.id
        if i.assignee != None:
            print "Assignee:",i.assignee.login
            one = i.assignee.login
        else:
            one = "None"
        if i.user != None:
            print "User:",i.user.login
            two = i.user.login
        else:
            two = "None"
        
        print "Adding an edge from:",one,"to:",two
        graph.add_edge(str(one),str(two))
        
        # We should look at the comments on the pull request, but a pull request is automatically translated
        # as an issue, so we are already looking at the issue comments
   
    print "-----"
  
 

    return


if __name__ == '__main__': 
    pass
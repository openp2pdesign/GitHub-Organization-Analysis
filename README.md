GitHub Organization Analysis
============================

Simple python scripts for analyzing a GitHub organization


** Usage: **

GitHub API limits last events to 300, if you want to mine more events you can download archives with all the data from githubarchive.org with the script *githubarchive-analysis.py* that will download all the data and create a folder with a *events.json* file that can be opened with the next script
*python githubarchive-analysis.py*

For general statistics visualization:
*python organization_stats.py*

For social network analysis (no problem with the API limits here at the moment):
*python organization_repositories_social_mining_weighted.py*


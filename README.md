# PyPlayground by Kevo

This is a collection of miscellaneous Python utilities built using online classes and many helpful references from around the web. Many of these utilities and games are straight-up copy/pasted from StackOverflow posts and Python community forums. I plan to clean up and organized this repo over time. I use the IntelliJ PyCharm IDE for development.

# Project Dependencies

```
$ sudo python3 -m ensurepip
$ pip3 --version
$ pip3 install pytest
$ pytest --version
$ pip3 install pylint

# UI Dependencies
$ pip3 install kivy

# AI and Data Science Dependencies
$ pip3 install torch
$ pip3 install matplotlib

# I don't remember what these do, but I installed them :)
$ pip3 install django
$ pip3 install flask
```

# PyCharm Interpreter Setup

To fix "unresolved references" errors in individual python packages, you'll need to right click directories with module imports, right click, and select "Mark Directory As... Sources Root"  

Inspect the `.idea/misc.xml` file and confirm that the jdk-name is "Python 3.7", and not "Python 3.7 (Project Name)".  

Inspect the `.idea/Project.iml` file and confirm there is an order entry for:  
```
<orderEntry type="jdk" jdkName="Python 3.7" jdkType="Python SDK" />
```

## Git Workflow References

Useful git commands for quickly traversing repos:  
```
# Display your git configuration
git config --list
git config --global -l

# Display all remote branches
git branch --remote

# Concise view of git history
git log --oneline

# Visual graph of git history
git log --oneline --graph --all --decorate --abbrev-commit

# See how many lines of code you've changed
git diff --shortstat

# Pushing from a local repository to GitHub hosted remote
git remote add origin git@github.com:USERNAME/REPO-NAME.git

# Clone your fork to your local machine
git clone git@github.com:USERNAME/FORKED-PROJECT.git

# Creating a new remote branch
git checkout master
git pull
git checkout -b pr-new-feature
git push -u origin pr-new-feature

# Delete a remote branch
git push origin :pr-merged-feature

# Remove a git ignored file that is being tracked
git rm -r --cached .
git add .

# Stash your local changes
git add .
git stash save "Implement a new whizbang feature"
git stash apply stash@{1}

# Preview your stashed changes
git stash list
git stash show -p stash@{1}

# Un-commit and stage changes from most recent commit
git reset --soft HEAD~1
```

## GitHub Standard Fork & Pull Request Workflow  
* Github pull request reviews documentation: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews  
* Useful link about project forks: https://gist.github.com/Chaser324/ce0505fbed06b947d962  
* Great YouTube video tutorial "Creating a Simple Github Pull Request" by Jake Vanderplas: https://www.youtube.com/watch?v=rgbCcBNZcdQ  

```
# Show which Git branches are tracking remote and upstream (source repo forked from)
git branch -vv

# Keeping a fork up-to-date
git remote add upstream git://github.com/ORIGINAL-USERNAME/FORKED-PROJECT.git
git fetch upstream
git pull upstream master

# List all remote pull requests
git ls-remote origin 'pull/*/head'

# Fetch a specific pull request into a local branch and with a custom name
git fetch origin pull/50/head:pr-new-feature

# Fetch a pull request from a fork repo and patch it as a local branch
git fetch git@github.com:username/ForkedPaymentApp.git refs/pull/50/head:pr-forked-feature
```

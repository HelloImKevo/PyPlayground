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

###YamDB API
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Documentation](#Documentation)
## General info
This project is simple social network about reviewing all titles in the workd :smiley_cat: with API.
	
## Technologies
Project is created with:
 * requests==2.26.0
 * django==2.2.16
 * djangorestframework==3.12.4
 * PyJWT==2.1.0
 * pytest==6.2.4
 * pytest-django==4.4.0
 * pytest-pythonpath==0.7.3
 * djangorestframework-simplejwt==4.7.2
 * django-filter==21.1

	
## Setup
To run this project, install it locally using npm:

```
$ cd ../api_yamdb
$ py venv vnev
$ . venv/Scrpits/Activate (. bin/Scripts/Activate)
$ pip install -r 'requarements.txt'
$ cd api_yamdb
$ py manage.py runserver

**optianly you can import DB from csv files**
**type py manage.py importcsv --help for more info**

$ py manage.py importcsv
```

## Documentation
You can find all paths with description in .../redoc

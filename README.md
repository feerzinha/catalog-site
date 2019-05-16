# Server setup

### Public IP Address: 52.70.226.141

### Configurations:

- SSH Port to 2200 

- HTTP Port to 80

- Check `requirements.txt` to install essential packages 

### Access

Public IP Address: 52.70.226.141
Grader: grader
Password: grader
Passphrase: udacity

To login, use: ssh grader@52.70.226.141 -p 2200 -i linuxCourse


### Server Components

- Apache2
- Database SQLite
- wsgi
- Flask


# Project Documentation

This is a project from Udacity - Full Stack Developer Nanodegree. It is a sports catalog website, that shows categories and items from each categories.

The site administrators (at this moment, just need to be logged with a google account) can add, edit and delete categories and items.

To run this project

1. Navigate to the Catalog-Project directory inside the vagrant environment

2. run `python database_setup.py` to create the database

3. run `python database_items.py` to populate the database

4. run `python catalog_project.py` and navigate to localhost:5000 in your browser

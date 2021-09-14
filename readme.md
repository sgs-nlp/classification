{% if False %}

# Introduction

In this project, we intend to create smart tools that can be used as an intelligent assistant in language problems in
systems. The language processed in this system is Persian. And the programming language used is Python.

![Default Home View](./static/screenshots/home.png?raw=true "Title")

### Main tools

* Text Similarity

* Keywords Extraction

* Text Classification

* etc.

# Usage

To use and source code of our program in your local, you must run our project.
The implementation method is as follows:

### Existing virtualenv

    $ virtualenv my_env
    $ source (to/path)/my_env/bin/activate
    (my_env)$

### No virtualenv

    $ pip install virtualenv
    $ virtualenv my_env
    $ source (to/path)/my_env/bin/activate
    (my_env)$
# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/USERNAME/{{ project_name }}.git
    $ cd {{ project_name }}

Activate the virtualenv for your project.

Install project dependencies:

    (my_env)$ pip install -r requirements.txt

Then simply apply the migrations:

    (my_env)$ python manage.py migrate

You can now run the development server:

    (my_env)$ python manage.py runserver

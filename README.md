# CAPSTONE PROJECT

## Summary

This a project review app, where we have reviewers and projects and we have sales manager to oversee them and supervisor 
to manage the reviewers and view projects and a project manager where they can assign reviewers to projects
also add projects or remove them.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from a potential frontend server. 

## Database Setup
With Postgres running, initialize the the database
```bash
createdb capstone
createdb capstone_test
```

iuyhkuytnmjjg,.kjhfjhg7yhnmhg## Running the server

From within the `/` directory first ensure you are working using your created virtual environment.

Please also set the database URL (sample script assumes postgres runs on port 5432)

To run the server locally, execute:

```bash
source setup.sh && flask run
```

the production project is available at https://fsdn-capstore.herokuapp.com

you can find the postman collection within the source files.

## Authentication

the tokens are already provided in the setup.sh file.

### User Roles

#### Sales Manager

Can view projects and reviewers

#### Supervisor

A Supervisor extends the permissions of the Sales Manager by adding and deleting reviewers from the database. He/She can also modify reviewers and projects

#### Project Manager

The Project Manager extends the permissions of the Supervisor by adding or deleting projects from the database,
also project manager can assign reviewers to projects and vise versa.

## API Documentation

you can find the documentation in details [here](https://documenter.getpostman.com/view/75324/T1LQfk9R)

## Errors

### 422
unprocessable e.g. trying to update a record that does not exist 
```json
{
    "error": 422,
    "message": "unprocessable",
    "success": false
}
```
 ### 406
 
when we can't create new resource in db 
 ```json
{
    "error": 406,
    "message": "Could not create new resource",
    "success": false
}
```
Defined Error handlers:
  - 400 - Bad reqest
  - 401 - token expired / invalid claims / invalid header
  - 403 - unauthorized
  - 404 - Resource not found
  - 422 - Unprocessable entity
  - 500 - Internal Server error
  - 406 - Could not create a resource
  
Sample Response for 404
```
{
  "error": 404, 
  "message": "Resource was not found", 
  "success": false
}
```


## Running tests

to the run the test execute:

```bash
dropdb capstone_test                                                      
createdb capstone_test
source setup.sh && python3 testcapstone.py 
```
 
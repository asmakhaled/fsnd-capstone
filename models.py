from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import os
 

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy( )

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename
    variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    print("lets drop and create the db", db)
    db.drop_all()
    db.create_all()

# db_drop_and_create_all()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}

class Project(db.Model):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    reviewers = db.relationship(
        'Reviewer',
        secondary="assignments")

    def __init__(self, length, genre, name):
        self.length = length
        self.genre = genre
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'length': self.length,
          'genre': self.genre,
          'reviewers': [x.name for x in self.reviewers]
        }



class Reviewer(db.Model):
    __tablename__ = 'reviewers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    projects = db.relationship(
      'Project',
      secondary="assignments" )

    def __init__(self, name, age, email, salary):
        self.email = email
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'email': self.email,
          'projects': [x.name for x in self.projects]
        }

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewers.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    user = db.relationship(Reviewer, backref=db.backref("assignments", cascade="all, delete-orphan"))
    product = db.relationship(Project, backref=db.backref("assignments", cascade="all, delete-orphan"))

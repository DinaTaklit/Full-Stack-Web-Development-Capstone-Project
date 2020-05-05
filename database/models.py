import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.model):
    __tablename__ = "movie"
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), nullable=false)
    # Release date
    release_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    '''
    get_movie(self)
        json form representation of the Movie model
    '''
    
    def get_movie(self):
        return {
            "id": self.id,
            "title": self.title,
            "realse_date": self.realse_date
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, realse_date=req_realse_date)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
        
    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title,realse_date=req_realse_date)
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    
    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Drink.id == id).one_or_none()
            movie.title = 'New Movie'
            movie.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.get_movie())


'''
Actor
a persistent actor entity, extends the base SQLAlchemy Model
'''

class Actor(db.model):
    __tablename__ = "actor"
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String name
    name = Column(String(80), nullable=false)
    # Integer age
    age = Column(Integer(), nullable=False)
    # String gender 
    name = Column(String(80), nullable=false)

    '''
    get_actor(self)
        json form representation of the Actor model
    '''
    
    def get_actor(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
        
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.get_actor())
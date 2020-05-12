import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app 
from models import db, db_drop_and_create_all, setup_db, Movie, Actor
from auth import AuthError, requires_auth
from sqlalchemy import Column, String, Integer, DateTime
import logging
from configparser import ConfigParser

# define the global vars 
database_name = "capstone_test.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_name))

casting_assistant_token = os.getenv('CASTING_ASSISTANT_JWT')
casting_director_token = os.getenv('CASTING_DIRECTOR_JWT')
executive_producer_token = os.getenv('EXECUTIVE_PRODUCER_JWT')

# define set authetification method 
def setup_auth(role):
    if role == 'casting_assistant':
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(casting_assistant_token)
            }
    elif role == 'casting_director':
        return {
            "Content-Type": "application/json",
            'Authorization': 'Bearer {}'.format(casting_director_token)
            }
    elif role == 'executive_producer':
        return {
            "Content-Type": "application/json",
            'Authorization': 'Bearer {}'.format(executive_producer_token)
            }

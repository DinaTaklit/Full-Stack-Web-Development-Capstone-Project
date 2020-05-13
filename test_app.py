import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app 
from database.models import db, db_drop_and_create_all, setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth
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
#Define the test case class for the application (or section of the application, for larger applications).
class CastingTestCase(unittest.TestCase):
    #Define and implement the setUp function. It will be executed before each test and is where you should initialize the app and test client, as well as any other context your tests will need. The Flask library provides a test client for the application, accessed as shown below.
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()      
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        
        self.new_actor = {
            "name": "Test Acotor",
            "age": 24,
            "gender":"female"
        }
        self.new_movie = {
            "title":"Test Movie"
        }
        #binds the app to the current context 
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all() 
            
    #Define the tearDown method, which is implemented after each test. It will run as long as setUp executes successfully, regardless of test success.
    def tearDown(self):
        """ Executed after each test """
        pass 
    
    
    #Define your tests. All should begin with "test_" and include a doc string about the purpose of the test. In defining the tests, you will need to:
    #1. Get the response by having the client make a request
    #2. Use self.assertEqual to check the status code and all other relevant operations.
    # def test_given_behavior(self):
    #     """Test ____________ """
    #     res = self.client().get('/')
    #     self.assertEqual(res.status_code, 200)
    
    
    ################################################
    #####           Actor Tests                #####
    ################################################
    
    # test get actors end points 
    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers=setup_auth("casting_assistant"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        
    def test_get_actors_casting_director(self):
        res = self.client().get('/actors', headers=setup_auth("casting_director"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))  
    
    def test_get_actors_executive_producer(self):
        res = self.client().get('/actors', headers=setup_auth("executive_producer"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))  
        
    def test_401_get_actor_fail(self):
        res = self.app.get('/actors', headers=setup_auth(''))
        self.assertEqual(res.status_code, 401)
    
    # test post actors end points      
    def test_post_actor_casting_assistant(self):
        res = self.app.post('/actors', json=self.new_actor,
                            headers=setup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)    
               
    def test_post_actor_casting_director(self):
        res = self.app.post('/actors', json=self.new_actor, headers=setup_auth('casting_director'))
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        
    def test_post_actor_executive_producer(self):
        res = self.app.post('/actors', json=self.new_actor, headers=setup_auth('executive_producer'))
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
    
#Run the test suite, by running python test_file_name.py from the command line.
if __name__ == "__main__":
    unittest.main()
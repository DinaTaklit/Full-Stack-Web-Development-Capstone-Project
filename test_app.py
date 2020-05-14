import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app 
from database.models import db, db_drop_and_create_all, setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth
from sqlalchemy import Column, String, Integer, DateTime
import logging
from setup import CASTING_ASSISTANT_JWT, CASTING_DIRECTOR_JWT, EXECUTIVE_PRODUCER_JWT
# define the global vars 
database_name = "capstone_test.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_name))


casting_assistant_token = CASTING_ASSISTANT_JWT
casting_director_token = CASTING_DIRECTOR_JWT
executive_producer_token = EXECUTIVE_PRODUCER_JWT

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
        self.app.config['TESTING'] = True ## add it to fix Error 500
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['DEBUG'] = False
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
    
    # test get actors end point
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
        res = self.client().get('/actors', headers=setup_auth(''))
        self.assertEqual(res.status_code, 401)
    
    # test post actors end point     
    def test_post_actor_casting_assistant(self):
        res = self.client().post('/actors', json=self.new_actor,
                            headers=setup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 403)    
               
    def test_post_actor_casting_director(self):
        res = self.client().post('/actors', json=self.new_actor, headers=setup_auth('casting_director'))
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        
    def test_post_actor_executive_producer(self):
        res = self.client().post('/actors', json=self.new_actor, headers=setup_auth('executive_producer'))
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        
    def test_422_post_actors_fail(self):
        res = self.client().post('/actors', json={}, headers=setup_auth('casting_director'))
        data = json.loads(res.data)  
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        
    # test patch actors end point 
    def test_patch_actor_casting_assistant(self):
        res = self.client().patch('/actors/1', json={'age':25},
                             headers=setup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 403)
        
        
    def test_patch_actor_casting_director(self):
        res = self.client().post('/actors', json=self.new_actor,
                             headers=setup_auth('casting_director'))
        res = self.client().patch('/actors/1', json={'age':25},
                             headers=setup_auth('casting_director'))
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none() 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.get_actor()['age'], 25)
        
    def test_patch_actor_executive_producer(self):
        res = self.client().patch('/actors/1', json={'age':25},
                             headers=setup_auth('executive_producer'))       
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none() 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.get_actor()['age'], 25)
    
    def test_404_patch_actor_fail(self):
        res = self.client().patch('/actors/100', json={},
                             headers=setup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test delete actors end point   
    def test_delete_actor_casting_assistant(self):
        res = self.client().delete('/actors/1', headers=setup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 403)

    def test_delete_actor_casting_director(self):
        res = self.client().delete('/actors/1', headers=setup_auth('casting_director'))
        data = json.loads(res.data)   
        actor = Actor.query.filter(Actor.id == 1).one_or_none()      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['deleted']), 1)
        self.assertEqual(actor,None)
        
    def test_delete_actor_executive_producer(self):
        res = self.client().post('/actors', json=self.new_actor, headers=setup_auth('executive_producer'))
        res = self.client().delete('/actors/1', headers=setup_auth('executive_producer'))
        data = json.loads(res.data)   
        actor = Actor.query.filter(Actor.id == 1).one_or_none()      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['deleted']), 1)
        self.assertEqual(actor,None)
    
    def test_401_delete_actor_fail(self):
        res = self.client().delete('/actors/1', headers=setup_auth(''))
        self.assertEqual(res.status_code, 401)
  
      
    ################################################
    #####           Movie Tests                #####
    ################################################
    # test get movies end point
    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies', headers=setup_auth("casting_assistant"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        
    def test_get_movies_casting_director(self):
        res = self.client().get('/movies', headers=setup_auth("casting_director"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))  
    
    def test_get_movies_executive_producer(self):
        res = self.client().get('/movies', headers=setup_auth("executive_producer"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))  
             
    def test_401_get_movie_fail(self):
        res = self.client().get('/movies', headers=setup_auth(''))
        self.assertEqual(res.status_code, 401)
    
    # test post movies end point      
    def test_post_movie_casting_assistant(self):
        res = self.client().post('/movies', json=self.new_movie,
                            headers=setup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)    
               
    def test_post_movie_casting_director(self):
        res = self.client().post('/movies', json=self.new_movie, headers=setup_auth('casting_director'))
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 401)
        
    def test_post_movie_executive_producer(self):
        res = self.client().post('/movies', json=self.new_movie, headers=setup_auth('executive_producer'))
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        
    def test_422_post_movies_fail(self):
        res = self.client().post('/actors', json={}, headers=setup_auth('casting_director'))
        data = json.loads(res.data)  
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)  

    # test patch movies end points 
    def test_patch_movie_casting_assistant(self):
        res = self.client().patch('/movies/1', json={'title':'updated_movie'},
                             headers=setup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 403)
        
        
    def test_patch_movie_casting_director(self):
        res = self.client().post('/movies', json=self.new_movie,
                            headers=setup_auth('executive_producer'))
        res = self.client().patch('/movies/1', json={'title':'updated_movie'},
                            headers=setup_auth('casting_director'))
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none() 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.get_movie()['title'], 'updated_movie')
        
    def test_patch_movie_executive_producer(self):
        res = self.client().patch('/movies/1', json={'title':'updated_movie'},
                             headers=setup_auth('executive_producer'))     
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none() 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.get_movie()['title'], 'updated_movie')
    
    def test_404_patch_movie_fail(self):
        res = self.client().patch('/movies/100000', json={},
                             headers=setup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    # test delete movies end point   
    def test_delete_movie_casting_assistant(self):
        res = self.client().delete('/movies/1', headers=setup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 403)

    def test_delete_movie_casting_director(self):
        res = self.client().delete('/movies/1', headers=setup_auth('casting_director'))
        self.assertEqual(res.status_code, 403)
  
    def test_delete_movie_executive_producer(self):
        res = self.client().delete('/movies/1', headers=setup_auth('executive_producer'))
        data = json.loads(res.data)   
        movie = Movie.query.filter(Movie.id == 1).one_or_none()      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['deleted']), 1)
        self.assertEqual(movie,None)
    
    def test_401_delete_movie_fail(self):
        res = self.client().delete('/movies/1', headers=setup_auth(''))
        self.assertEqual(res.status_code, 401)

#Run the test suite, by running python test_file_name.py from the command line.
if __name__ == "__main__":
    unittest.main()
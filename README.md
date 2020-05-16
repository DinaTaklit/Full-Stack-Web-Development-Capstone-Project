# Casting Agency Capstone Project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Casting Agency Specifications

### Models

- Movies with attributes title and release date
- Actors with attributes name, age and gender

### Endpoints

- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/
  
### Roles

- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

### Tests

- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.
  
## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

- The `--reload` flag will detect file changes and restart the server automatically.
- Or you can directly run it with `python app.py` and everythin will be done automatically.

> Note: To run the app and correctly you need to export all the global variables for the auth and token. To do so if you are in linux evn it is easy you have just to the setup bash script. But in windows to make things more easier do everything from bash.

## Export global vars from Setup.sh

In windows env to make things easier use git bash which allows you to run bash commend.

1. Enable conda within git to do so add `conda.sh` to your **bach profile** or whatever the name of your bash profile.

  ```bash
  echo ". C:/Users/user/Anaconda3/etc/profile.d/conda.sh" >> ~/.bash_profile
  ```

  Now the conda should run in your git :D.

2. Activate  your conda env in your git bash for ex `conda activate myenv`
3. Run the script file using this commnad `. script.sh` wihting th folder where the script exists.
  
Check those questions on stack overflow links for more details

- [Anaconda and Git Bash in Windows - conda: command not found](https://stackoverflow.com/questions/54501167/anaconda-and-git-bash-in-windows-conda-command-not-found)
  
- [Running .sh script in Git Bash](https://stackoverflow.com/questions/36401147/running-sh-scripts-in-git-bash/61832248#61832248)

## Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:movies`
   - `get:actors`
   - `post:movies`
   - `post:actors`
   - `patch:movies`
   - `patch:actors`
   - `delete:movies`
   - `delete:actors`
  
6. Create new roles for:
    - Casting Assistant
        - can  `get:movies get:actors`
    - Casting director
       - All permissions a Casting Assistant has and…
       - Add or delete an actor from the database `post:actors delete:actors`
       - Modify actors or movies `patch:actors delete:movies`
    - Executive producer
       - Can perform all actions  

7. Test your endpoints with [Postman](https://getpostman.com).
    - Register 3 users - assign the Casting Assistant role to the first one, Casting Director role to the second and Executive porducer to the last one.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./capstone-project.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the included one to be able to run with your own jwt :).

> Note: to sign in and get the tokens for the diff roles type on your broser:
> 
> ```http
> https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
> ```
> Like for example in my case:
>```http
>https://coffee-shop-application.auth0.com/authorize?audience=capstone-app&response_type=token&client_id=p1U7BG6MaJxHOSEJzrdNwFsVrC9CZjnR&redirect_uri=https://capstone-casting-agency-app.herokuapp.com/ 
>```  


## Testing
To run the tests, run

```
python test_app.py
```
## Deploy the application on heroku

To depoloy your application follow this document => [Deploy an application on Heroku](https://github.com/DinaTaklit/HerokuSample/blob/master/README.md). he is a fast resume, after installing heroku, and heroku CLI

1. `hroku login`to loggin into heroku
2. Update requirements.txt each time you add dependency `pip freeze > requirements.txt`
3. Setting up your environement varibales in `setup.sh`
4. Install **Gunicorn** (a pure-Python HTTP server for WSGI applications used to deploy the app) => `pip install gunicorn`
5. Create `Procfile` include one line to instruct Heroku correctly for us: `web: gunicorn app:app`. app is the  application's entry point var in th `main` module.
6. To allow heroku run all your migrations to the database you have hosted on the platforme, your application need to include `manage.py` file. Create `manage.py` file that should contain the following code
  
  ```python
  from flask_script import Manager
  from flask_migrate import Migrate, MigrateCommand

  from app import APP
  from database.models import db

  migrate = Migrate(APP, db)
  manager = Manager(APP)

  manager.add_command('db', MigrateCommand)


  if __name__ == '__main__':
      manager.run()

  ```

7. Istall those package to run the migrations

  ```bash
  pip install flask_script
  pip install flask_migrate
  pip install psycopg2-binary
  ```

> Remember to freeze the dependecies every after you installing those packages.

8. Run our local migrations using our `manage.py` file, to mirror how Heroku will run behind the scenes for us when we deploy our app

  ```bash
  python manage.py db init
  python manage.py db migrate
  python manage.py db upgrade
  ```

9. Your file structure should contains those files
  
  ```bash
  > migrations
  .gitignore
  app.py
  manage.py
  models.py
  Procfile
  requirements.text
  Setup.sh
  ```

 > Note the versions folder under migrations is empty. Once you push this repo to git it will not included since it is empty. and once you deploy and try to run the last command for migration will got and error theire is no folder named versions. To avoid this issue create an empty inside migrations/versions folder `touch keep` so once you stage and push your work it will upload  also versions folder :).

10. Crete heroku app => `heroku create name_of_your_app`
    
11. Add git remote for heroku to local repo that you get from the previous command or you can get it from heroku web site on by clicking on your app there and click on settings. You will find it there :). => `git remote add heroku heroku_git_url` 

> If you the previous commend through an error fata remote already exsit because you created a previous app just run thsi commend and you fix the issue => `git remote set-url heroku heroku_git_url`

12. Add postgresql add on for your database => `heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application`
    
> Run the under command to check your config vars in heroku `heroku config --app name_of_your_application`

13. Push it :D. After you push everything to your git now push from git to heroku => `git push heroku master`

> To check if you everthing is staged use `git status`

14. Run migrations: Once your app is deployed, run migrations by running: `heroku run python manage.py db upgrade --app name_of_your_application`

And that is it all. Congratulation :D. Now we have a live app :D. Open it from the heroku dashboard and see it live :D. Make additional requests using curl or Postman as you build your application and make more complex endpoints :).

## API Reference

### Getting Started

- **Base URL**: Base URL: Actually, this app can be run locally and it is hosted also as a base URL using heroku (the deplyed application URL is : https://capstone-casting-agency-app.herokuapp.com/). The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- **Authentication**: This version of the application require authentication or API keys using Auth0 (Ps: The setup is givin in setup Auth0 section)

### Error Handling

Errors are returned as JSON object in the following format:

```json
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return four(04) error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not allowed
- 422: Not Processable
- 401: AuthError Unauthorized error
- 403: AuthError Permission not found
  
### Endpoints

- GET '/actors'
- GET '/movies'
- POST '/actors'
- POST '/movies'
- PATCH '/actors/{actor_id}'
- PATCH '/movies/{movie_id}'
- DELETE '/actors/{actor_id}'
- DELETE '/movies/{movie_id}'

#### GET /actors

- Require the `get:actors` permission
- Returns a list of actors

```json
return jsonify({
        'success': True,
        'actors': actors
    })
```

#### GET /movies

- Require the `get:movies` permission
- Returns a list of movies
  
```json
return jsonify({
        'success': True,
        'movies': movies
    })
```

#### POST /actors

- Require the `post:actors` permission
- Create a new row in the actors table
- Contain the actor.get_actor data representation
returns status code 200 and json `{"success": True, "actors": actor}` where actor an array containing only the newly created actor or appropriate status code indicating reason for failure

Here is a returned sample fromat

```json
{
  "actors": [
    {
      "age": 24,
      "gender": "Female",
      "id": 1,
      "name": "Actor 1"
    }
  ],
  "success": true
}
```

#### POST /movies

- Require the `post:movies` permission
- Create a new row in the movies table
- Contain the movie.get_movie data representation
returns status code 200 and json `{"success": True, "movies": movie}` where movie an array containing only the newly created movie or appropriate status code indicating reason for failure.

Here is a result sample format:

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Thu, 14 May 2020 14:02:13 GMT",
      "title": "Movie 1"
    }
  ],
  "success": true
}
```

#### PATCH /actors/<actor_id>

- Require the 'patch:actors' permission
- Update an existing row in the actors table
- Contain the actor.get_actor data representation
returns status code 200 and json `{"success": True, "actors": actor}` where actor an array containing only the updated actor
or appropriate status code indicating reason for failure

He is a sample for a  modified actor in a format:

```json
{
  "actors": [
    {
      "age": 25,
      "gender": "female",
      "id": 1,
      "name": "Updated Actor 1"
    }
  ],
  "success": true
}
```

#### PATCH /movies/<movie_id>

- Require the `patch:movies` permission
- Update an existing row in the movies table
- Contain the movie.get_movie data representation
returns status code 200 and json `{"success": True, "movies": movie}` where movie an array containing only the updated movie
or appropriate status code indicating reason for failure

Here is an example of the modified movie  in a format: 

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Thu, 14 May 2020 14:02:13 GMT",
      "title": "Updated Movie 1"
    }
  ],
  "success": true
}
```

#### DELETE /actors/<actor_id>

- Require the `delete:actors` permission
- Delete the corresponding row for `<actor_id>` where `<actor_id>` is the existing model id
- Respond with a 404 error if `<actor_id>` is not found
- Returns status code 200 and json `{"success": True, "deleted": actor_id}` where id is the id of the deleted record
or appropriate status code indicating reason for failure

```json
return jsonify({
    "success": True,
    "deleted": actor_id
})
```

#### DELETE /movies/<movie_id>

- Require the `delete:movies` permission
- Delete the corresponding row for `<movie_id>` where `<movie_id>` is the existing model id
- Respond with a 404 error if `<movie_id>` is not found
- Returns status code 200 and json `{"success": True, "deleted": id}` where id is the id of the deleted record
or appropriate status code indicating reason for failure

```json
return jsonify({
    "success": True,
    "deleted": movie_id
})
```

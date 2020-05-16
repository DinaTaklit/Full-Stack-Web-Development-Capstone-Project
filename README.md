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

## Testing
To run the tests, run
```
python test_app.py
```
# API Reference 

## Getting Started 

- **Base URL**: Base URL: Actually, this app can be run locally and it is hosted also as a base URL using heroku (the deplyed application URL is : https://capstone-casting-agency-app.herokuapp.com/). The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- **Authentication**: This version of the application require authentication or API keys using Auth0 (Ps: The setup is givin in setup Auth0 section)

## Error Handling

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
  
## Endpoints

- GET '/actors'
- GET '/movies'
- POST '/actors'
- POST '/movies'
- PATCH '/actors/{actor_id}'
- PATCH '/movies/{movie_id}'
- DELETE '/actors/{actor_id}'
- DELETE '/movies/{movie_id}'

### GET /actors

- Require the `get:actors` permission
- Returns a list of actors

```json
return jsonify({
        'success': True,
        'actors': actors
    })
```

### GET /movies

- Require the `get:movies` permission
- Returns a list of movies
  
```json
return jsonify({
        'success': True,
        'movies': movies
    })
```

### POST /actors

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

### POST /movies

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


### PATCH /actors/<actor_id>

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

### PATCH /movies/<movie_id>

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

### DELETE /actors/<actor_id>

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

### DELETE /movies/<movie_id>

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

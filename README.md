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

- **Base URL**: Base URL: Actually, this app can be run locally and it is hosted also as a base URL using heroku (the heroku URL is ). The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
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

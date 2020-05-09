import json
from flask import request, _request_ctx_stack,abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'coffee-shop-application.auth0.com'  # The domaine url 
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone-app' # The api audiance
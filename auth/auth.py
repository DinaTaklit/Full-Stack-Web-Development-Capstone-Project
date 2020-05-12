import json
from flask import request, _request_ctx_stack,abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

import logging
from logging import FileHandler, Formatter

AUTH0_DOMAIN = 'coffee-shop-application.auth0.com'  # The domaine url 
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone-app' # The api audiance

## Configure the logging
logging.basicConfig(filename='error.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')


## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header

'''
@Done implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    # print("request.headers", request.headers)
    auth = request.headers.get('Authorization', None) # get the authorization part of the request headers
 
    if not auth: # the header is missing
        logging.info('Authorization header is missing')
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
    parts = auth.split() # the header must contain the bearer + token
    if parts[0].lower() != 'bearer': 
        logging.info('invalid_header, Authorization header must start with "Bearer')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    
    elif len(parts) == 1:
        logging.info('invalid_header, Token not found')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        logging.info('invalid_header, Authorization header must be bearer token.')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)
    token = parts[1]
    return token

'''
@Done implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:actor')
        payload: decoded jwt payload
    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        logging.info('invalid_claims, Permissions not included in JWT.')
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        logging.info('unauthorized, Permission not found.')
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True



'''
@Done implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/',
                options={'verify_exp':False}
            )
            print("\n payload => \n{}\n".format(payload))

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)
'''
@Done implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            print("\nWe got the token :D\n")
            try:
                payload = verify_decode_jwt(token)
                print("\npayload\n", payload)
            except:
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)  
        return wrapper
    return requires_auth_decorator
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Movie, Actor

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    #db_drop_and_create_all()

    # ROUTES
    '''
    @Done implement endpoint
        /
            it should be a public endpoint
        returns status code 200 and json {"success": True, "message": "hello world"}
        or appropriate status code indicating reason for failure
    '''

    @app.route('/')
    def home():
        return jsonify({
            'success': True,
            'message': 'hello world'
        })


    '''
    @Done implement endpoint
        GET /actors
            it should require the 'get:actors' permission
        returns status code 200 and json {"success": True, "actors": actors}
        where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''
    @app.route('/acotors')
    def get_actors():
        data = Actor.query.all()
        actors= list(map(Actor.get_actor, data))
        if actors is None or len(actors) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': acotors
        })



    # Error Handling
    '''
    @Done implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

    '''
    @Done implement error handler for 404
        error handler should conform to general task above
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
        
    '''
    @Done implement error handler for 400
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    '''
    @Done implement error handler for 405
    '''
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    '''
    @Done implement error handler for 422
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
    @Done implement error handler for AuthError
        error handler should conform to general task above
    '''
    # @app.errorhandler(AuthError)
    # def auth_error(error):
    #     return jsonify({
    #         "success": False,
    #         "error": error.status_code,
    #         "code": error.error['code'],
    #         "message": error.error['description']
    #     }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    #APP.run(host='0.0.0.0', port=8080, debug=True)
    APP.run(debug=True)
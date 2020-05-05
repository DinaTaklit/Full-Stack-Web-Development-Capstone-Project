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
    db_drop_and_create_all()

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


    return app


APP = create_app()

if __name__ == '__main__':
    #APP.run(host='0.0.0.0', port=8080, debug=True)
    APP.run(debug=True)
import os
from flask import Flask, jsonify, abort, request
from models import setup_db, Reviewer, Project
from flask_cors import CORS
from auth import AuthError, requires_auth

# full stack capstone
def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/reviewers')
    @requires_auth(permission='read:reviewers')
    def get_reviewers(jwt):
        reviewers = Reviewer.query.all()
        reviewers_formated = [reviewer.format() for reviewer in reviewers]
        result = {
            "success": True,
            "Reviewers": reviewers_formated
        }
        return jsonify(result)

    @app.route('/reviewers', methods=['POST'])
    @requires_auth('write:reviewers')
    def create_reviewer(jwt):
        body = request.get_json()

        try:
            name = body.get('name', None)
            email = body.get('email', None)

            reviewers = Reviewer.query.filter(Reviewer.name.like(name)).count()
            print("current", reviewers)
            if reviewers > 0:
                raise AuthError({
                    'code': 'Bad request',
                    'description': "This reviewer is already existent"
                }, 400)
            reviewer = Reviewer(
                name=name, email=email)
            reviewer.insert()
            return jsonify({
                'success': True,
                'reviewers': [reviewer.format()]
            })
        except Exception as e:
            print("exception error post reviewer", e)
            print(e)
            if isinstance(e, AuthError):
                raise e
            abort(406)

    @app.route('/reviewers/<int:id>', methods=['PATCH'])
    @requires_auth('update:reviewers')
    def update_reviewer(jwt, id):
        body = request.get_json()
        name = body.get('name', None)
        email = body.get('email', None)

        try:
            reviewer = Reviewer.query.get(id)

            if reviewer is None:
                abort(404)

            if name is not None:
                reviewer.name = name
            if email is not None:
                reviewer.email = email

            reviewer.update()

            return jsonify({
                'success': True,
                'reviewers': [reviewer.format()]
            })
        except Exception as e:
            print("exception error post reviewer", e)
            print(e)
            if isinstance(e, AuthError):
                raise e
            abort(406)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app


app = create_app()


'''
    handle autherization errors
'''
@app.errorhandler(AuthError)
def handleAuthError(error):
    print("auth erorr", error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), 401

@app.errorhandler(406)
def handleError406(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 406,
        "message": "Could not create new resource"
    }), 406


if __name__ == '__main__':
    app.run()
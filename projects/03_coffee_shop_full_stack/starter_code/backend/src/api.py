import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success':True,
            'drinks': [drink.short() for drink in drinks]
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_detail(jwt):
    drinks = Drink.query.all()
    try:
        return jsonify({
            'success':True,
            'drinks': [drink.long() for drink in drinks]
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):

    body = request.get_json()

    if not ('title' in body and 'recipe' in body):
        abort(422)

    title = body.get('title')
    recipe = body.get('recipe')

    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()],
        })

    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):

    drink = Drink.query.get(id)

    if drink:
        try:

            body = request.get_json()

            title = body.get('title')
            recipe = body.get('recipe')

            if title:
                drink.title = title
            if recipe:
                drink.title = recipe

            drink.update()

            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })
        except:
            abort(422)
    else:
        abort(404)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):

    drink = Drink.query.get(id)

    if drink:
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)
    else:
        abort(404)

## Error Handling

'''
Error handling for bad request.
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    'success': False,
                    'error': 400,
                    'message': 'bad request'
                    }), 400


'''
Error handling for resource not found.
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    'success': False,
                    'error': 404,
                    'message': 'resource not found'
                    }), 404


'''
Error handling for method not allowed.
'''
@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
                    'success': False,
                    'error': 405,
                    'message': 'method not allowed'
                    }), 405


'''
Error handling for unprocessable entity.
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    'success': False,
                    'error': 422,
                    'message': 'unprocessable'
                    }), 422


'''
Error handling for internal server error.
'''
@app.errorhandler(500)
def server_error(error):
    return jsonify({
                    'success': False,
                    'error': 500,
                    'message': 'internal server error'
                    }), 500


'''
Error handling for service unavailable errors
for instance database connection errors.
'''
@app.errorhandler(503)
def service_unavailable(error):
    return jsonify({
                    'success': False,
                    'error': 503,
                    'message': 'service unavailable'
                    }), 503


'''
Error handling for Authentication errors.
Returns 401, 403 or 400 error codes.
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    'success': False,
                    'error': error.status_code,
                    'message': error.error['description']
                    }), error.status_code
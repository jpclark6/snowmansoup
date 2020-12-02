import os
import uuid

import boto3

from flask import request, jsonify
from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)

def parse_user_id(req):
    return req.headers['Authorization'].split()[1]

@app.route('/sunshine')
def melt_one_soup():
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    return jsonify('Melted a snowman')

@app.route('/summer')
def melt_all_soup():
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unquthorized'), 401

    return jsonify('All the snowmen melted')
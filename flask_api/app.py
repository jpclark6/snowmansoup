import os
import uuid

import boto3

from flask import request, jsonify
from flask_lambda import FlaskLambda

from boto3.dynamodb.conditions import Key

REGION = os.environ['REGION_NAME']
TABLE_NAME = os.environ['TABLE_NAME']

app = FlaskLambda(__name__)

dynamodb = boto3.resource('dynamodb', region_name=REGION)

def db_table(table_name=TABLE_NAME):
    return dynamodb.Table(table_name)

def parse_user_id(req):
    return req.headers['Authorization'].split()[1]

@app.route('/soups')
def fetch_soups():
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    table_response = db_table().query(KeyConditionExpression=Key('userId').eq(user_id))
    return jsonify(table_response['Items'])

@app.route('/soups', methods=('POST',))
def create_soup():
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    soup_id = str(uuid.uuid4())
    soup_data = request.get_json()
    soup_data.update(userId=user_id, soupId=soup_id)
    table = db_table()
    table.put_item(Item=soup_data)
    table_response = table.get_item(Key={'userId': user_id, 'soupId': soup_id})
    return jsonify(table_response['Item']), 201

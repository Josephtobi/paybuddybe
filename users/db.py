import requests
from dotenv import load_dotenv
import os
import json
from django.contrib.auth.hashers import make_password, check_password


load_dotenv()


def add(data):

    url = "https://eu-west-2.aws.data.mongodb-api.com/app/data-davkf/endpoint/data/v1/action/insertOne"

    headers = {
        'api-key': os.getenv('MONGO'),
        'Accept': 'application/json',
        'Content-Type': 'application/ejson'
    }

    payload = {
        "dataSource": "Paybuddybe",
        "database": "app_db",
        "collection": "user_db",
        "document": data
    }

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))

    return response.json()


def search(data):
    url = "https://eu-west-2.aws.data.mongodb-api.com/app/data-davkf/endpoint/data/v1/action/findOne"

    headers = {
        'api-key': os.environ['MONGO'],
        'Accept': 'application/json'
    }

    payload = {
        "dataSource": "Paybuddybe",
        "database": "app_db",
        "collection": "user_db",
        "filter": data
    }

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))

    return response.json()


def reg(data):
    res = search({'email': data['email']})
    if res == None:

        payload = {
            'email': data['email'],
            'fullname': data['fullname'],
            'dob': data['dob'],
            'country': data['country'],
            'is_active': data['is_active'],
            'email_verified': data['email_verified'],
            'hashed_password': make_password(data['password']),

        }
        add(payload)
        return True
    else:
        return False


def login_user(data):
    res = search({'email': data['email']})
    print(res)
    if res == None:
        return False
    user = res['document']
    return check_password(data['password'], user['hashed_password'])


def fetch_user(email):
    res = search({'email': email})
    user = res['document']
    user.pop('hashed_password')
    user.pop('_id')

    return user

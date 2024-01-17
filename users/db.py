import requests
import os
import json
from django.contrib.auth.hashers import make_password, check_password

url = "https://paybuddydb-marp.harperdbcloud.com"

headers = {
    'Content-Type': 'application/json',
    'Authorization': os.environ['db_auth']
}


def reg(data, url=url, headers=headers):
    # print(data)
    payload = {
        'operation':
        'insert',
        'schema':
        'db',
        'table':
        'Users',
        'records': [{
            'email': data['email'],
            'fullname': data['fullname'],
            'dob': data['dob'],
            'country': data['country'],
            'is_active': data['is_active'],
            'email_verified': data['email_verified'],
            'password': make_password(data['password'])
        }]
    }
    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=json.dumps(payload))

    if (len(json.loads(response.text.encode('utf8'))['skipped_hashes']) == 0):
        return False

    # print(json.loads(response.text.encode('utf8'))['skipped_hashes'])


def check_user(data, url=url, headers=headers):
    # print(data)
    payload = {
        'operation': 'search_by_hash',
        'schema': 'db',
        'table': 'Users',
        'hash_values': [data['email']],
        'get_attributes': ['password']
    }
    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=json.dumps(payload))
    hashed = json.loads(response.text.encode('utf8'))[0]['password']
    return check_password(data['password'], hashed)


def fetch_user(email, url=url, headers=headers):
    payload = {
        'operation': 'search_by_hash',
        'schema': 'db',
        'table': 'Users',
        'hash_values': [email],
        'get_attributes': ['*']
    }
    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=json.dumps(payload))
    ans = json.loads(response.text.encode('utf8'))[0]
    ans.pop('password')

    return ans

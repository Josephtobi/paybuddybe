import jwt
from datetime import datetime, timedelta
import os


def Accesstoken(email):
    payload = {
        'email': email,
        'token': 'access',
        'exp': datetime.now() + timedelta(minutes=5)
    }
    accesstoken = jwt.encode(payload,
                             os.environ['SECRET_KEY'],
                             algorithm="HS256")
    return accesstoken


def Refreshtoken(email):
    payload = {
        'email': email,
        'token': 'refresh',
        'exp': datetime.now() + timedelta(hours=24)
    }
    refreshtoken = jwt.encode(payload,
                              os.environ['SECRET_KEY'],
                              algorithm="HS256")
    return refreshtoken


def checktoken(token):
    try:
        payload = jwt.decode(token,
                             os.environ['SECRET_KEY'],
                             algorithms=["HS256"])
        now = int(datetime.now().timestamp())

        if now > payload['exp']:
            return 1
        else:
            return 2
    except:
        return 0


def getemail(token):
    payload = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=["HS256"])
    return [payload['email'], payload['token']]

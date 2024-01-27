from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from . import serializers, tokens
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .db import *
from django.contrib.auth.hashers import check_password


# Create your views here.
@swagger_auto_schema(methods=['post'],
                     request_body=serializers.RegisterSerializer)
@api_view(['POST'])
def register(request):
    body = json.loads(request.body)
    serializer = serializers.RegisterSerializer(data=body)
    if serializer.is_valid():
        # print(body)
        a = reg(body)
        if a:
            access = tokens.Accesstoken(body['email'])
            refresh = tokens.Refreshtoken(body['email'])
            mes = {
                "message": 'User registered',
                'Accesstokens': access,
                'Refreshtokens': refresh
            }
        else:
            mes = {"message": 'User already exists'}

        return Response(mes)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['post'],
                     request_body=serializers.LoginSerializer)
@api_view(['POST'])
def login(request):
    body = json.loads(request.body)
    serializer = serializers.LoginSerializer(data=body)
    if serializer.is_valid():
        a = login_user(body)
        if a:
            access = tokens.Accesstoken(body['email'])
            # refresh = tokens.Refreshtoken(body['email'])
            data = fetch_user(body['email'])
            mes = {
                "message": 'User Logged in',
                "data": data,
                'Accesstokens': access,
            }
            return Response(mes)
        else:
            mes = {
                "message": 'wrong password',
            }
            return Response(mes, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh(request):
    body = json.loads(request.body)
    a = tokens.checktoken(body['token'])
    if a == 0:
        mes = {
            "message": 'invalid token',
        }
        return Response(mes, status=status.HTTP_401_UNAUTHORIZED)
    if a == 1:
        mes = {
            "message": 'expired token',
        }
        return Response(mes, status=status.HTTP_401_UNAUTHORIZED)
    elif a == 2:
        email = tokens.getemail(body['token'])[0]
        token_type = tokens.getemail(body['token'])[1]
        if token_type != 'refresh':
            mes = {
                "message": 'invalid token, send refresh tokens instead',
            }
            return Response(mes, status=status.HTTP_401_UNAUTHORIZED)

        access = tokens.Accesstoken(email)
        mes = {"message": 'Token Refreshed', 'Accesstokens': access}
        return Response(mes)


# @api_view(['POST'])
# def test(request):
#     body = json.loads(request.body)
#     a = fetch_user(body['email'])

#     return Response(a)

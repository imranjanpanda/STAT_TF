import json
import jwt
import bcrypt
import boto3
from services import login, register, verify, logout
from utils import builder

def lambda_handler(event, context):
    print(event)
    print(context)
    
    if event['path'] == "/register" and event['httpMethod'] == "POST":
        response = register.register(
            event['name'],
            event['username'],
            event['password']
        )
        return response

    elif event['path'] == "/login" and event['httpMethod'] == "POST":
        response = login.login(event['username'], event['password'])
        return builder.build_response(200, response)

    elif event['path'] == "/verify" and event['httpMethod'] == "GET":
        response = verify.verify(event['username'], event['token'])
        return builder.build_response(200, response)

    elif event['path'] == "/logout" and event['httpMethod'] == "POST":
        response = logout.logout(event['username'], event['token'])
        return builder.build_response(200, response)
    else:
        return builder.build_response(400, {
            'message': f"{event['httpMethod']} is not allowed in {event['path']} route"
        })

import bcrypt
import boto3
from utils import builder
from utils import auth

# Initialize DynamoDB client


SALT_ROUNDS = 8

def register(name, username, password):
    try:
        if not name or not username or not password:
            return builder.build_response(400, {"message": "Missing required fields"})
        print(username)
        user = get_user(username)
        if user:
            return builder.build_response(400, {"message": "User already exists"})

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(SALT_ROUNDS))
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        # Create new user in DynamoDB
        table.put_item(
            Item={
                'username': username,
                'name': name,
                'password': hashed_password.decode('utf-8'),
            }
        )

        # Generate JWT token for the registered user
        token = auth.generate_token(username)

        return builder.build_response(200, {
            "message": "User registered successfully",
            "token": token
        })

    except Exception as e:
        return builder.build_response(500, {"message": f"Internal server error: {str(e)}"})

def get_user(username):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        # Query DynamoDB for existing user
        response = table.get_item(Key={'username': username})
        print(response)
        print(username)
        return response.get('Item')
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")

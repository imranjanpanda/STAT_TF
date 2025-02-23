import bcrypt
import boto3
from utils import builder
from utils import auth

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('users')

def login(username, password):
    try:
        if not username or not password:
            return builder.build_response(400, {"message": "Missing required fields"})

        user = get_user(username)
        if not user:
            return builder.build_response(400, {"message": "User not found"})

        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return builder.build_response(400, {"message": "Incorrect password"})

        # Generate JWT token for the authenticated user
        token = auth.generate_token(username)

        return builder.build_response(200, {
            "message": "Login successful",
            "token": token
        })

    except Exception as e:
        return builder.build_response(500, {"message": f"Internal server error: {str(e)}"})

def get_user(username):
    try:
        # Query DynamoDB for user
        response = table.get_item(Key={'username': username})
        return response.get('Item')
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")

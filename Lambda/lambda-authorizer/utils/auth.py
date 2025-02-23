import jwt
import time

# Secret key for signing tokens
# Function to get the secret key from AWS Parameter Store
def get_secret_key():
    ssm = boto3.client('ssm')
    try:
        parameter = ssm.get_parameter(Name='STAT_SECRET', WithDecryption=True)
        return parameter['Parameter']['Value']
    except (BotoCoreError, ClientError) as e:
        raise Exception(f"Error retrieving secret key: {str(e)}")

# Secret key for signing tokens
SECRET_KEY = get_secret_key()
# Generate JWT token
def generate_token(username):
    try:
        payload = {
            "username": username,
            "exp": int(time.time()) + 3600  # Token expires in 1 hour
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise Exception(f"Error generating token: {str(e)}")

# Verify JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    except Exception as e:
        raise Exception(f"Error verifying token: {str(e)}")

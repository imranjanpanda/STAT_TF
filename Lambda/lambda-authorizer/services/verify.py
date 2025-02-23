from utils import builder
from utils import auth

def verify(username, token):
    try:
        # Verify the JWT token
        payload = auth.verify_token(token)
        if not payload or payload.get("username") != username:
            return 400
        
        return 200

    except Exception as e:
        return 500

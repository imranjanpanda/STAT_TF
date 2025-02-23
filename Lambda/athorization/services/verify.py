from utils import builder
from utils import auth

def verify(username, token):
    try:
        # Verify the JWT token
        payload = auth.verify_token(token)
        if not payload or payload.get("username") != username:
            return builder.build_response(400, {"message": "Invalid or expired token"})
        
        return builder.build_response(200, {"message": "Token verification successful"})

    except Exception as e:
        return builder.build_response(500, {"message": f"Internal server error: {str(e)}"})

from utils import builder
from utils import auth

def logout(username, token):
    try:
        # Verify the JWT token to ensure the user is valid
        payload = auth.verify_token(token)
        if not payload or payload.get("username") != username:
            return builder.build_response(400, {"message": "Invalid or expired token"})

        # Logic to handle logout (e.g., invalidate token if needed)
        # In this simple example, we'll just return a successful logout message
        return builder.build_response(200, {"message": "Logout successful"})

    except Exception as e:
        return builder.build_response(500, {"message": f"Internal server error: {str(e)}"})

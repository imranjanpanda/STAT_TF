import json
from services import verify
def lambda_handler(event, context):
    print(event)
    print(context)
    method_arn = event.get("methodArn")      # Get API Gateway method ARN
    if event['httpMethod'] == "GET":
        headers = event.get("headers", {})
        username = headers.get("username", "Guest")
        token = headers.get("token", "")
        print(username, token, method_arn, headers)
        response = verify.verify(username, token)
    # Validate the token (Replace this with your JWT validation logic)
    if response == 200:  
        return generate_policy(username, "Allow", method_arn, {"username":username})
    else:
        return generate_policy("username", "Deny", method_arn, {})

def generate_policy(principal_id, effect, resource, context=None):
    auth_response = {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }

    if context:
        auth_response["context"] = context  # Add extra context data (optional)

    return auth_response

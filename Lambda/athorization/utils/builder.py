import json

def build_response(status_code, body):
    try:
        return {
            'statusCode': status_code,
            'body': json.dumps(body),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"message": f"Error building response: {str(e)}"}),
            'headers': {
                'Content-Type': 'application/json',
            },
        }

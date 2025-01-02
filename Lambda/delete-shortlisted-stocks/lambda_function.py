import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Shortlisted_Stocks')
    
    try:
        item = json.loads(event['body'])
        key = {
            'ID': item['ID'],
            'Date': item['Date']  
        }
        
        table.delete_item(Key=key)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item deleted successfully'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error deleting item: {str(e)}"
        }

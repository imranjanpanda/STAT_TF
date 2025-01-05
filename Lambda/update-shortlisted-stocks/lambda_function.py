import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Custom JSON encoder to handle Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Shortlisted_Stocks')
    print("Received event: ")
    print(event)
    print("*********************")
    try:
        item = json.loads(event['body'], parse_float=Decimal)
        print("Parsed item: ")
        print(item)
        print("*********************")
        # Assuming the table has a composite primary key: 'ID' (partition key) and 'Date' (sort key)
        key = {
            'ID': item['ID'],
            'Date': item['Date']  # Replace 'Date' with the actual sort key attribute name
        }
        print("Key: ")
        print(key)
        print("*********************")
        
        update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in item if k not in key)
        expression_attribute_values = {f":{k}": v for k, v in item.items() if k not in key}
        expression_attribute_names = {f"#{k}": k for k in item if k not in key}
        print("Update Expression: ")
        print(update_expression)
        print("Expression Attribute Values: ")
        print(expression_attribute_values)
        print("Expression Attribute Names: ")
        print(expression_attribute_names)
        print("*********************")

        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': json.dumps({'message': 'Item updated successfully'}, cls=DecimalEncoder)
        }
    
    except Exception as e:
        print("Exception: ")
        print(e)
        print("*********************")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': f"Error updating item: {str(e)}"
        }

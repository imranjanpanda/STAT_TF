import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# Custom JSON encoder to handle Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert Decimal to float or int
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Shortlisted_Stocks')
    
    # Define fields to retrieve
    fields = [
        "ID", "Date", "Action", "Active", "Entry_Price", "File_Path", 
        "Instrument_Token", "Notes", "RR", "SL_Price", "Statergy_Name", 
        "Stock_Name", "Target", "Timeframe"
    ]
    
    # Extract optional filters from the event input
    filters = event.get('filters', {})  # Default is an empty dictionary
    
    # Construct filter expression
    filter_expression = None
    for key, value in filters.items():
        if key in fields:
            condition = Attr(key).eq(value)
            filter_expression = condition if filter_expression is None else filter_expression & condition

    try:
        # Query DynamoDB table with or without filters
        if filter_expression:
            response = table.scan(FilterExpression=filter_expression)
        else:
            response = table.scan()
        
        # Extract the relevant fields from each item
        items = response.get('Items', [])
        selected_items = [{field: item.get(field) for field in fields} for item in items]

        # Serialize the response with Decimal handling
        return {
            'statusCode': 200,
            'body': json.dumps(selected_items, cls=DecimalEncoder)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error fetching records: {str(e)}"
        }

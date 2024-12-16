import boto3
import json
import os

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    user_id = event["requestContext"]["authorizer"]["principalId"]
    
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(
        KeyConditionExpression="UserId = :userId",
        ExpressionAttributeValues={":userId": user_id},
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps({"tasks": response.get("Items", [])}),
    }

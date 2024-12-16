import boto3
import json
import os

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]


def lambda_handler(event, context):
    user_id = event["requestContext"]["authorizer"]["principalId"]
    task_id = event["pathParameters"]["taskId"]

    table = dynamodb.Table(TABLE_NAME)
    table.delete_item(Key={"UserId": user_id, "TaskId": task_id})

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Task deleted successfully"}),
    }

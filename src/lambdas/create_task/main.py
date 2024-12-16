import boto3
import json
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
sqs = boto3.client("sqs")
TABLE_NAME = os.environ["TABLE_NAME"]
QUEUE_URL = os.environ["QUEUE_URL"]


def lambda_handler(event, context):
    user_id = event["requestContext"]["authorizer"]["principalId"]
    body = json.loads(event["body"])

    task_id = str(uuid.uuid4())
    task = {
        "UserId": user_id,
        "TaskId": task_id,
        "Title": body["title"],
        "Description": body.get("description", ""),
        "DueDate": body["due_date"],
        "Status": "Pending",
        "AttachmentURL": None,
    }

    # Save task in DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=task)

    # Send a reminder message to SQS
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(
            {
                "UserId": user_id,
                "TaskId": task_id,
                "Title": body["title"],
                "Description": body["due_date"],
            }
        ),
    )

    return {
        "statusCode": 201,
        "body": json.dumps(
            {"message": "Task created successfully", "task_id": task_id}
        ),
    }

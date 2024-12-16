import json
import boto3
import datetime
import os
from boto3.dynamodb.conditions import Attr

# Initialize AWS clients
dynamodb = boto3.resource("dynamodb")
sqs = boto3.client("sqs")

# Environment variables
DYNAMODB_TABLE = os.environ["TABLE_NAME"]
SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]


def lambda_handler(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)
    current_date = datetime.datetime.utcnow()
    max_date = current_date + datetime.timedelta(days=5)

    # Scan DynamoDB for tasks due within the next 5 days
    response = table.scan(
        FilterExpression=Attr("DueDate").between(
            current_date.strftime("%m/%d/%Y"), max_date.strftime("%m/%d/%Y")
        )
    )

    tasks = response.get("Items", [])

    # Publish tasks to SQS
    for task in tasks:
        sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(task))

    print(f"Published {len(tasks)} tasks to SQS.")
    return {"statusCode": 200, "body": f"Published {len(tasks)} tasks to SQS."}

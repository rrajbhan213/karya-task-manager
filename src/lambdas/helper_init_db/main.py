import json
import boto3
from botocore.exceptions import ClientError
import cfnresponse


def lambda_handler(event, context):
    print(json.dumps(event, indent=2))

    dynamo_table_name = event["ResourceProperties"]["DynamoTableName"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(dynamo_table_name)

    item = {
        "group": "karya-group",
        "policy": {
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:execute-api:us-east-1:746669197921:*/*/GET/api/status",
                        "arn:aws:execute-api:us-east-1:746669197921:*/*/*/api/tasks*",
                        "arn:aws:execute-api:us-east-1:746669197921:*/*/*/api/tasks/*",
                    ],
                    "Sid": "Karya-API",
                }
            ],
            "Version": "2012-10-17",
        },
    }

    try:
        table.put_item(Item=item)
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except ClientError as e:
        print(f"Error: {e}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {})

import os
import boto3
import base64
import json

# Initialize S3 and DynamoDB resources
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
S3_BUCKET_NAME = os.environ["BUCKET_NAME"]
TABLE_NAME = os.environ["TABLE_NAME"]


def lambda_handler(event, context):
    try:
        print(event)
        # Get task_id from pathParameters
        task_id = event["pathParameters"]["taskId"]

        # Get user_id from request context (from an authorizer)
        user_id = event["requestContext"]["authorizer"]["principalId"]

        # Extract the binary file content and file name from headers
        file_content = event["body"]
        if event.get("isBase64Encoded"):
            file_content = base64.b64decode(event["body"])

        file_name = event["headers"].get(
            "X-File-Name", f"{task_id}.bin"
        )  # Default to task_id.bin if no file name

        # Define S3 key
        s3_key = f"{user_id}/{task_id}/{file_name}"

        # Upload the file to S3
        upload_to_s3(file_content, s3_key)

        # Generate S3 URL
        s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        # Update DynamoDB task with the file URL
        update_task_with_attachment(user_id, task_id, s3_url)

        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "File uploaded and task updated successfully",
                    "AttachmentURL": s3_url,
                }
            ),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Failed to upload file", "error": str(e)}),
        }


def upload_to_s3(file_content, s3_key):
    """Upload the file to S3."""
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key, Body=file_content)
    print(f"File uploaded to S3 with key: {s3_key}")


def update_task_with_attachment(user_id, task_id, attachment_url):
    """Update the DynamoDB task with the file URL."""
    table = dynamodb.Table(TABLE_NAME)
    table.update_item(
        Key={"UserId": user_id, "TaskId": task_id},
        UpdateExpression="SET AttachmentURL = :url",
        ExpressionAttributeValues={":url": attachment_url},
        ReturnValues="UPDATED_NEW",
    )
    print(f"Task {task_id} updated with AttachmentURL: {attachment_url}")

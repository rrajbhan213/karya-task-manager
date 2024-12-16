import boto3
import json
import os

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]


def lambda_handler(event, context):
    try:
        user_id = event["requestContext"]["authorizer"]["principalId"]
        task_id = event["pathParameters"]["taskId"]
        body = json.loads(event["body"])

        table = dynamodb.Table(TABLE_NAME)
        update_expression = "SET "
        expression_values = {}
        expression_attribute_names = {}

        for key, value in body.items():
            # Use ExpressionAttributeNames for reserved keywords
            attribute_name = f"#{key}" if is_reserved_keyword(key) else key
            update_expression += f"{attribute_name} = :{key}, "
            expression_values[f":{key}"] = value
            if is_reserved_keyword(key):
                expression_attribute_names[attribute_name] = key

        # Remove the trailing comma and space
        update_expression = update_expression.rstrip(", ")

        # Prepare the update item parameters
        update_params = {
            "Key": {"UserId": user_id, "TaskId": task_id},
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": expression_values,
        }

        if expression_attribute_names:
            update_params["ExpressionAttributeNames"] = expression_attribute_names

        # Perform the update
        table.update_item(**update_params)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Task updated successfully"}),
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Failed to update task", "error": str(e)}),
        }


def is_reserved_keyword(keyword):
    """Check if a keyword is reserved in DynamoDB."""
    reserved_keywords = {"STATUS"}
    return keyword.upper() in reserved_keywords

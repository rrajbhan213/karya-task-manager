import os
import boto3
import json

sns = boto3.client("sns")
TABLE_NAME = os.environ["TABLE_NAME"]
TOPIC_ARN = os.environ["TOPIC_ARN"]


def lambda_handler(event, context):
    print(event)
    for record in event["Records"]:
        message = json.loads(record["body"])
        user_id = message["UserId"]
        task_id = message["TaskId"]
        due_date = message["DueDate"]
        title = message.get("Title")

        # Construct reminder message
        reminder_message = f"""
        Reminder: You have a task due soon!
        Task ID: {task_id}
        User ID: {user_id}
        Title: {title}
        Due Date: {due_date}
        """

        sns.publish(
            TopicArn=TOPIC_ARN, Message=reminder_message, Subject="Task Reminder"
        )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Reminders processed successfully"}),
    }

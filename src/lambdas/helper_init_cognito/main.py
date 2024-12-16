import boto3
from botocore.exceptions import ClientError
import cfnresponse


def lambda_handler(event, context):
    user_pool_id = event["ResourceProperties"]["UserPoolId"]
    username = event["ResourceProperties"]["CognitoUserName"]
    password = event["ResourceProperties"]["CognitoUserPassword"]

    print(f"username: {username}")

    cognito_client = boto3.client("cognito-idp")

    try:
        # Create the user
        create_user_params = {
            "UserPoolId": user_pool_id,
            "Username": username,
            "TemporaryPassword": password,
        }
        response_create_user = cognito_client.admin_create_user(**create_user_params)
        print(response_create_user)

        # Set the user password to permanent
        set_password_params = {
            "UserPoolId": user_pool_id,
            "Username": username,
            "Password": password,
            "Permanent": True,
        }
        response_set_password = cognito_client.admin_set_user_password(
            **set_password_params
        )
        print(response_set_password)

        # Send SUCCESS response back to CloudFormation
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except ClientError as e:
        print(e.response["Error"]["Message"])
        # Send FAILED response back to CloudFormation
        cfnresponse.send(event, context, cfnresponse.FAILED, {})

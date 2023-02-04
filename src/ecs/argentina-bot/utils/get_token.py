import boto3
import json


def get_secret(secret_name) -> dict:
    '''Function that gets values from AWS Credentials Manager'''

    # https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html
    client = boto3.client('secretsmanager', region_name='us-west-2')
    secrets = client.get_secret_value(SecretId=secret_name)
    return json.loads(secrets['SecretString'])

BOT_TOKEN = get_secret('telegram-bot-credentials')['BOT_TOKEN']

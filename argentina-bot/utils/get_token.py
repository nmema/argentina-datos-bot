import boto3
import json


def get_secret(secret_name) -> dict:
    '''function that gets values from AWS Credentials Manager'''
    session = boto3.session.Session(profile_name='saml')
    client = session.client('secretsmanager', region_name='us-west-2')
    secrets = client.get_secret_value(SecretId=secret_name)
    return json.loads(secrets['SecretString'])

BOT_TOKEN = get_secret('telegram-bot-credentials')['BOT_TOKEN']

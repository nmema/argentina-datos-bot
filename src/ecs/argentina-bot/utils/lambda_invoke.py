import boto3
import json
import os


def get_data(lambda_name: str, payload: dict) -> dict:
    client = boto3.client('lambda', region_name='us-west-2')
    
    response = client.invoke(
        FunctionName=os.environ[lambda_name],
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    return json.loads(response['Payload'].read())

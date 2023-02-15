from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_dynamodb as ddb
)

from backend.ecs.infrastructure import ECS


class Backend(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        inflation_lambda = _lambda.Function(
            self, 'argcd-inflation',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('src/lambda'),
            handler='inflation.lambda_handler'
        )

        change_rates_lambda = _lambda.Function(
            self, 'argcd-change-rates',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('src/lambda'),
            handler='change_rates.lambda_handler',
            timeout=Duration.seconds(10)
        )

        emae_lambda = _lambda.Function(
            self, 'argcd-emae',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('src/lambda'),
            handler='emae.lambda_handler',
            timeout=Duration.seconds(10)
        )

        feedback_table = ddb.Table(
            self, 'argcd-feedback',
            partition_key={'name': 'user_id', 'type': ddb.AttributeType.NUMBER},
            sort_key={'name': 'chat_date', 'type': ddb.AttributeType.STRING}
        )

        ecs = ECS(
            self, 'ArgentinaConDatosECS',
            lambda_inf=inflation_lambda,  # TODO: How to handle with multiple lambdas
            lambda_chr=change_rates_lambda,
            lambda_ema=emae_lambda,
            table = feedback_table
        )

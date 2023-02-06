from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda
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

        ecs = ECS(
            self, 'ArgentinaConDatosECS',
            downstream=inflation_lambda  # TODO: How to handle with multiple lambdas
        )

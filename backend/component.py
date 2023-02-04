from constructs import Construct
from aws_cdk import (
    Stack
)

from backend.ecs.infrastructure import ECS


class Backend(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecs = ECS(
            self, 'ArgentinaConDatosECS'
        )

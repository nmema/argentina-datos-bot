from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_lambda as _lambda,
    aws_dynamodb as ddb
)


class ECS(Construct):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 downstream: _lambda.IFunction, 
                 table: ddb.ITable,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(
            self, 'ArgentinaConDatosRole',
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com')
        )
        
        role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    'secretsmanager:GetSecretValue',
                    'lambda:InvokeFunction'
                ],
                resources=['*']
            )
        )

        # https://docs.amazonaws.cn/en_us/vpc/latest/userguide/nat-gateway-scenarios.html
        vpc = ec2.Vpc(
            self, 'argentina-con-datos-vpc',
            max_azs=1
        )

        ecs_cluster = ecs.Cluster(
            self, 'argentina-con-datos-cluster',
            vpc=vpc
        )

        image = ecs.ContainerImage.from_asset(
            directory='./src/ecs'
        )

        task_definition = ecs.FargateTaskDefinition(
            self, 'argentina-con-datos-task-definition',
            execution_role=role,
            task_role=role,
            cpu=1024,
            memory_limit_mib=3072
        )

        container = task_definition.add_container(
            'telegram-bot',
            image=image,
            logging=ecs.AwsLogDriver(stream_prefix='ArgentinaDatosContainer'),
            environment={
                'LAMBDA_INFLATION': downstream.function_name,
                'DYNAMODB_FEEDBACK': table.table_name
            }
        )
        
        service = ecs.FargateService(
            self, 'argentina-con-datos-service',
            cluster=ecs_cluster,
            task_definition=task_definition,
            desired_count=1
        )

        table.grant_read_write_data(service.task_definition.task_role)

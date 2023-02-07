## Arquitectura

A continuación se presenta el diagrama con la arquitectura de la solución propuesta:

<p align="center">
  <img src="/backend/img/diagram.png"/>
</p>

Se desarrolló el IaC utilizando el CDK de Python para luego deployar los recursos a través de CloudFormation. En el stack se compone:
- [Lambda function](https://github.com/nmema/aws-solutions-architect-project/blob/main/backend/component.py#L16-L21) que le pega a la [API de Series de Tiempo del Gobierno](https://datosgobar.github.io/series-tiempo-ar-api/).
- [DynamoDB table](https://github.com/nmema/aws-solutions-architect-project/blob/main/backend/component.py#L23-L27) donde se registran los comentarios realizados.
- [ECS](https://github.com/nmema/aws-solutions-architect-project/blob/main/backend/ecs/infrastructure.py) con un cluster corriendo adentro un servicio con el Bot de Telegram.

ECS fue desplegado en una red privada mediante un Nat Gateway en una red pública ([caso de uso](https://docs.amazonaws.cn/en_us/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-gateway-overview)), esto le permite tener con conexión a internet. Para recibir tráfico se tuvo que provisionar una regla de ACL.

### Proceso
El Bot inicializa tomando por [Secrets Manager](https://github.com/nmema/aws-solutions-architect-project/blob/main/src/ecs/argentina-bot/utils/get_token.py#L9-L11) el token de acceso a la API de Telegram, y espera por comandos.
- Cuando recibe el comando `/inflacion` se hace la llamada a la [función lambda](https://github.com/nmema/aws-solutions-architect-project/blob/main/src/ecs/argentina-bot/app.py#L33-L37).
- Cuando recibe el comando `/comentario` se hace la llamada a la [tabla de dynamodb](https://github.com/nmema/aws-solutions-architect-project/blob/main/src/ecs/argentina-bot/app.py#L68-L76) para insertar los valores.

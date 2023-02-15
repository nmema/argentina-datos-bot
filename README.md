# Argentina con Datos Bot

## Introducción
En [Datos Argentina](https://datos.gob.ar/) se encuentran datasets con todo tipo de información de la Argentina. Puede que para acceder a ellas requieran varios pasos y debamos descargar mayor información de la necesaria. Por eso se desarrolló @ArgentinaDatosBot, un **bot de Telegram** al cuál podes realizarles consultas especificas y te responderá en cuestión de segundos!

Para charlar con él:
- desde la [web](https://web.telegram.org/k/#@ArgentinaDatosBot)
- desde el celular buscando @ArgentinaDatosBot 

Por el momento ofrece solamente tres comandos... pero nos gustaría que nuestro Bot siga creciendo! Por eso dejanos tu opinión en `/comentario` sobre qué otra información te gustaría ver. 


## Requisitos
- [Cuenta de AWS](https://aws.amazon.com/console/)
- [CDK de Python](https://docs.aws.amazon.com/cdk/api/v1/python/index.html)
- Guardar el TOKEN de acceso al Bot de Telegram en un secreto de Secrets Manager con el nombre `telegram-bot-credentials` con un secret key igual a `BOT_TOKEN`.

Luego una vez en la raíz del proyecto ejecutar
```
cdk deploy
```

Para eliminar los recursos de la cuenta.
```
cdk destroy
```

## Arquitectura

A continuación se presenta el diagrama con la arquitectura de la solución propuesta:

<p align="center">
  <img src="/img/diagram.png"/>
</p>

Se desarrolló el IaC utilizando el CDK de Python para luego deployar los recursos a través de CloudFormation. En el stack se compone:
- [Lambdas](https://github.com/nmema/argentina-datos-bot/blob/main/backend/component.py#L17-L38) que le pegan a la [API de Series de Tiempo del Gobierno](https://datosgobar.github.io/series-tiempo-ar-api/).
- [DynamoDB](https://github.com/nmema/argentina-datos-bot/blob/main/backend/component.py#L40-L44) donde se registran los comentarios realizados.
- [Elastic Container Service](https://github.com/nmema/argentina-datos-bot/blob/main/backend/ecs/infrastructure.py) con un cluster corriendo adentro un servicio con el Bot de Telegram.

ECS fue desplegado en una red privada mediante un Nat Gateway en una red pública ([caso de uso](https://docs.amazonaws.cn/en_us/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-gateway-overview)), esto le permite tener con conexión a internet. Para recibir tráfico se tuvo que provisionar una regla de ACL.

## Proceso
El Bot inicializa tomando por [Secrets Manager](https://github.com/nmema/argentina-datos-bot/blob/main/src/ecs/argentina-bot/utils/get_token.py#L9-L11) el token de acceso a la API de Telegram. Una vez finalizado, espera por los siguientes comandos:
- comando `/inflacion`, hace la llamada a la función lambda [inflation](https://github.com/nmema/argentina-datos-bot/blob/main/src/lambda/inflation.py).
- comando `/tiposdecambio`, hace la llamada a la función lambda [change_rates](https://github.com/nmema/argentina-datos-bot/blob/main/src/lambda/change_rates.py).
- comando `/emae`, hace la llamada a la función lambda [emae](https://github.com/nmema/argentina-datos-bot/blob/main/src/lambda/emae.py).
- comando `/comentario`, hace la [llamada](https://github.com/nmema/argentina-datos-bot/blob/main/src/ecs/argentina-bot/app.py#L133-L141) a la tabla de dynamodb para insertar los valores.

## ToDo
- Unit Testing.
- Definir un ELB delante del ECS y un ASG.

--------------

Proyecto realizado como trabajo final para la diplomatura [ITBA Cloud Architecture](https://innovacion.itba.edu.ar/educacion-ejecutiva/tic/cloud-architecture/)
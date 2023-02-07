# AWS Solutions Architect Project

### Introducción
En https://datos.gob.ar/ se encuentran datasets con todo tipo de información de la Argentina. Puede que acceder a ellas requieran varios pasos y debamos descargar mayor información de la necesaria. Por eso se desarrolló @ArgentinaDatosBot, un bot de Telegram al cuál podes realizarles consultas especificas y te responderá en cuestión de segundos! Contiene registros desde el 2016 en adelante.

Para charlar con él:
- desde la [web](https://web.telegram.org/k/#@ArgentinaDatosBot)
- desde el celular buscando @ArgentinaDatosBot 

Por el momento ofrece solamente un comando... pero nos gustaría que nuestro Bot siga creciendo! Por eso dejanos tu opinión en `/comentario` sobre qué otra información te gustaría ver. 


### Requisitos
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

Proyecto realizado como trabajo final para la diplomatura [ITBA Cloud Architecture](https://innovacion.itba.edu.ar/educacion-ejecutiva/tic/cloud-architecture/). Para conocer sobre la arquitectura del proyecto, haz click [aquí](https://github.com/nmema/aws-solutions-architect-project/tree/13-readme-explanation/backend#readme)

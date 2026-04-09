
La computación distribuida es un paradigma donde un sistema no está formado por una sola computadora, sino por varias computadoras o procesos que trabajan de manera coordinada para ejecutar una aplicación. Cada una de estas unidades de cómputo o procesos se denomina **nodo**.

En computación distribuida, se define a un **nodo** como un proceso o una máquina que participa en el sistema comunicándose con otros nodos. En el caso particular de ROS, un nodo será un proceso independiente que realiza una tarea específica dentro del sistema robótico y se comunica con otros nodos mediante mensajes. ^c70871

## Networking y middlewares

**Networking** es el conjunto de tecnologías, protocolos y prácticas que permiten que distintos nodos se conecten y comuniquen entre sí.
Por otro lado, un **middleware** es una capa intermedia de software que facilita la comunicación entre sistemas o aplicaciones.


## DDS

**DDS** es un middleware de networking que simplifica la programación de networking. Implementa un publish-suscribe pattern para enviar y recibir información, eventos y comandos a través de nodos.
### El modelo publish-suscribe

El patrón publish-suscribe es un patrón de mensajes en el cuál los emisores de mensajes, llamados **publicadores**, clasifican los mensajes en clases (o *topics*) y los envían sin la necesidad de saber que componentes los recibirán.
Los receptores de mensajes, llamados **suscriptores**, pueden suscribirse a uno o más *topics* y recibir los mensajes de esas clases, sin la necesidad de conocer a los publicadores.
Cualquier nodo puede ser un publicador, un suscriptor o ambos simultáneamente.

### El Domain ID

Un Domain ID es un identificador numérico que define un dominio de comunicación dentro de DDS. Cada nodo puede unirse a exactamente un Domain ID lo que le permitirá interactuar con el resto de nodos en ese dominio pero no con los que tengan un dominio diferente. Esto permite que haya muchos sistemas independientes en la misma red.

Por defecto, en ROS, todos los nodos utilizan el mismo Domain ID. Para prevenir interferencias entre distintos grupos de computadoras que ejecutan ROS 2 en la misma red, se recomienda configurar un Domain ID diferente para cada grupo.

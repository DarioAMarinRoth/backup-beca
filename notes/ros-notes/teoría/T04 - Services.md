
## 1. ¿Qué es un Servidor en ROS 2?

En ROS 2, un servidor es un componente de un **Nodo** que implementa el paradigma de comunicación de **Servicios**. Este modelo sigue una estructura de **cliente-servidor**, diseñada para interacciones donde un nodo (el cliente) envía una solicitud (request) a otro nodo (el servidor) y espera una respuesta (response).

### Características Principales

- **Comunicación Bidireccional:** A diferencia de otros modelos, los servicios permiten el envío de datos en la solicitud y la recepción de datos en la respuesta.
- **Asincronía en ROS 2:** Aunque en versiones anteriores de ROS los servicios eran predominantemente síncronos, en ROS 2 se recomienda el uso de clientes de servicio asíncronos para evitar el bloqueo del ciclo de control del nodo que realiza la llamada.
- **Respuesta Inmediata:** Están diseñados para cálculos rápidos o consultas de estado que no interfieran significativamente con el tiempo real del sistema.
- **Interfaz Definida:** Utilizan archivos `.srv` (Service Definition Language) que especifican claramente la estructura del mensaje de solicitud y el de respuesta.

--------------------------------------------------------------------------------

## 2. Diferencias con otros Tipos de Nodos y Comunicaciones

ROS 2 ofrece tres paradigmas principales de comunicación. Es fundamental entender cuándo utilizar un servidor de servicios frente a otros mecanismos.

|   |   |   |   |
|---|---|---|---|
|Característica|**Servicios (Servidor)**|**Temas (Topics)**|**Acciones (Actions)**|
|**Modelo**|Cliente-Servidor|Publicación-Suscripción|Cliente-Servidor (con retroalimentación)|
|**Flujo**|Bidireccional (Solicitud/Respuesta)|Unidireccional (Flujo de datos)|Bidireccional|
|**Sincronía**|Asíncrono (preferido en ROS 2)|Asíncrono|Asíncrono|
|**Duración**|Ejecución corta/rápida|Flujo continuo|Larga duración (segundos/minutos)|
|**Retroalimentación**|No (solo respuesta final)|No|Sí (progreso intermedio)|
|**Casos de uso**|Cambiar un parámetro, resetear un mapa|Datos de sensores (láser, cámara), comandos de velocidad|Navegación a un punto, mover un brazo robótico|

--------------------------------------------------------------------------------

## 3. Configuración de un Servidor con `rclpy`

La biblioteca **rclpy** permite crear servidores de servicios integrándolos directamente en la estructura de clases de un nodo. El método principal para esta tarea es `create_service`.

### El Método `create_service`

Este método se invoca usualmente dentro del constructor del nodo (`__init__`) para registrar el servicio en el grafo computacional.

#### Argumentos Principales

1. **srv_type:** Es el tipo de interfaz de servicio que se utilizará. Debe ser importado desde un paquete de interfaces (por ejemplo, `example_interfaces.srv`). Define la estructura de los datos.
2. **srv_name:** Una cadena de texto que define el nombre del servicio en el sistema (por ejemplo, `'/sum_numbers'`).
3. **callback:** La función o método que se ejecutará cada vez que el servidor reciba una solicitud. Esta función debe aceptar dos argumentos: `request` y `response`.

#### Argumentos Opcionales Interesantes

- **callback_group:** Permite asignar el servidor a un grupo de rellamada específico. Esto es crítico para el control de la ejecución y el manejo de la concurrencia en sistemas de tiempo real o nodos complejos que utilizan múltiples ejecutores.
- **qos_profile:** Aunque los servicios tienen perfiles de Calidad de Servicio (QoS) predeterminados para garantizar la entrega, es posible ajustarlos para necesidades específicas de red.

--------------------------------------------------------------------------------

## 4. Estructura de la Interfaz del Servicio (.srv)

Para que un servidor funcione, requiere una definición en un archivo `.srv`. Estos archivos se dividen en dos secciones separadas por tres guiones (`---`):

```text
# Ejemplo de archivo .srv
string input_data  # Solicitud (Request)
---
string output_data # Respuesta (Response)
```

El servidor recibe el objeto `request` con los campos definidos arriba y debe llenar y retornar el objeto `response` con los campos definidos abajo.

--------------------------------------------------------------------------------

## 5. Ejemplos Básicos

### Ejemplo A: Servidor Simple de Procesamiento de Cadenas

Este ejemplo muestra la lógica básica de un servidor que recibe un texto y devuelve una respuesta confirmando el procesamiento.

```python
# Importación de rclpy y la interfaz necesaria
from example_interfaces.srv import AddTwoInts # Ejemplo de tipo de servicio
import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service_node')
        # Configuración del servidor
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        # Lógica del servidor
        response.sum = request.a + request.b
        self.get_logger().info(f'Solicitud recibida: a={request.a}, b={request.b}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
```

### Ejemplo B: Servidor con Nombres y Namespaces

Siguiendo las convenciones de ROS 2, los nombres de los servicios pueden ser relativos, absolutos o privados. Al configurar un servidor, se debe tener en cuenta el espacio de nombres (namespace) para evitar interferencias en aplicaciones multi-robot.

- **Nombre absoluto:** `/robot1/reset_odom` (comienza con `/`).
- **Nombre relativo:** `reset_odom` (se expande según el namespace del nodo).
- **Nombre privado:** `~reset_odom` (incluye el nombre del nodo en la jerarquía).

--------------------------------------------------------------------------------

## 6. Monitoreo e Inspección

Una vez que el servidor está en ejecución, se pueden utilizar herramientas de línea de comandos (CLI) de ROS 2 para verificar su estado, las cuales son fundamentales para el diagnóstico:

1. **Listar servicios activos:**
2. **Ver el tipo de un servicio y sus nodos:**
3. **Identificar qué nodos ofrecen un servicio:**
4. _(Esto mostrará una sección de "Service Servers" con los servicios que el nodo está escuchando)._

Esta estructura garantiza que los servidores en ROS 2 actúen como unidades de cómputo reactivas, integradas de manera segura y modular en aplicaciones robóticas complejas.
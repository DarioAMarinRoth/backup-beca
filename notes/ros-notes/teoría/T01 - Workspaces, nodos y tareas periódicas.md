# Fundamentos de ROS 2 para la Creación de Nodos y Tareas Periódicas

Esta guía proporciona el marco conceptual necesario para comprender la arquitectura de ROS 2 (Robot Operating System 2), la gestión de espacios de trabajo, la creación de paquetes bajo el sistema de construcción `ament_python` y la implementación de lógica de ejecución en tiempo real mediante el uso de nodos y temporizadores (Timers).

## 1. Introducción a ROS 2 y su Arquitectura

ROS 2 es un **middleware** basado en un mecanismo de publicación/suscripción anónimo y de tipos fuertemente definidos que permite el paso de mensajes entre diferentes procesos. El núcleo de cualquier sistema ROS 2 es el **grafo de ROS (ROS graph)**, el cual representa la red de elementos que se comunican entre sí.

### Conceptos Fundamentales

- **Nodos (Nodes):** Es la unidad básica en ROS. Cada nodo debe encargarse de una tarea específica (manejar un dispositivo de hardware o computar un algoritmo). La modularidad permite que el sistema sea robusto; si un nodo falla, no necesariamente colapsa todo el grafo.
- **Interfaces:** Los nodos se comunican a través de interfaces como tópicos (flujos de datos), servicios (modelo cliente-servidor) y acciones (tareas de larga duración con retroalimentación).
- **Bibliotecas de Cliente (Client Libraries):** Permiten a los desarrolladores escribir código en diferentes lenguajes. Para Python, se utiliza `rclpy`, que ofrece una interfaz idiomática utilizando tipos y patrones nativos (como listas y objetos de contexto).

## 2. El Espacio de Trabajo (Workspace) y el Sistema de Archivos

Para desarrollar en ROS 2, es imperativo organizar el código en una estructura de directorios específica denominada **Workspace**.

### Estructura Típica de un Workspace

Un espacio de trabajo estándar (por ejemplo, `ros2_ws`) se organiza de la siguiente manera:

1. `**src/**`**:** Directorio donde reside el código fuente. Aquí se clonan o crean los paquetes.
2. `**build/**`**:** Almacena archivos intermedios generados durante la compilación.
3. `**install/**`**:** Contiene los ejecutables y archivos de configuración finales una vez compilado el paquete.
4. `**log/**`**:** Contiene información de registro sobre el proceso de compilación y ejecución.

### El Proceso de Sourcing

Para que una terminal reconozca los comandos de ROS 2 y los paquetes instalados, se debe ejecutar un archivo de configuración del entorno (`setup.bash`). Este proceso se conoce como **sourcing**:

- Entorno global: `source /opt/ros/<distribucion>/setup.bash`
- Entorno local (del workspace): `source install/local_setup.bash`

>[!Note]
>La distribución actual se llama `kilted`

>[!Note]
>Como estoy usando fish como shell, no puedo correr ese script directamente. Instalé un plugin para fish que se llama `bass` que me permite ejecutar comandos de bash.  
Para ejecutar cualquier comando de bash, solamente hay que anteponer `bass` al comando.

#### Automatizar el source

Si no se quiere hacer source cada vez que se abra una shell, se puede puede agregar el comando al script del startup del shell. El comando es cuestión es:
```shell
echo "source /opt/ros/kilted/setup.bash" >> ~/.bashrc
```

> [!note]
> Nuevamente como estoy usando fish el comando en mi caso sería:
> ```shell
> echo "bass source /opt/ros/kilted/setup.bash" >> ~/.config/fish/conf.d/ros.fish
> ```


## 3. Desarrollo de Paquetes con `ament_python`

Un paquete es un contenedor para el código de ROS 2. Cuando se desarrolla en Python, se utiliza el tipo de construcción `ament_python`.

### Comandos de Creación

Para crear un paquete desde el directorio `src/`, se utiliza la herramienta de línea de comandos de ROS 2:

```bash
ros2 pkg create --build-type ament_python <nombre_del_paquete> --node-name <nombre_del_nodo>
```

### Archivos Clave en un Paquete Python

|   |   |
|---|---|
|Archivo|Función|
|`package.xml`|Contiene metadatos como el nombre del paquete, versión, autor, licencia y dependencias (ej. `rclpy`).|
|`setup.py`|Define cómo se debe instalar el paquete y especifica los "entry points" (puntos de entrada) para los ejecutables de los nodos.|
|`setup.cfg`|Configuración necesaria para que `setuptools` encuentre los scripts.|
|`nombre_del_paquete/`|Directorio con el mismo nombre que el paquete donde se aloja el código fuente (`__init__.py` y los scripts de los nodos).|

## 4. Implementación de Nodos y Temporizadores (Timers)

Un nodo en Python se implementa típicamente como una clase que hereda de `rclpy.node.Node`.

### El Uso de Timers para Tareas Periódicas

En aplicaciones de hardware (como la lectura de registros Modbus), es fundamental ejecutar tareas de forma periódica sin bloquear el hilo principal de ejecución.

- **Ejecución No Bloqueante:** Un Timer permite que el nodo realice una acción (ej. imprimir en consola) a intervalos precisos mientras permanece disponible para escuchar otras instrucciones o procesar otros eventos simultáneamente.
- **Definición:** Dentro del constructor de la clase del nodo (`__init__`), se crea el Timer especificando el periodo (en segundos) y la función de retorno (callback) que se ejecutará cada vez que expire el tiempo.

### El Sistema de Registro (Logging)

ROS 2 proporciona un subsistema de logging para entregar mensajes a la consola, a archivos en disco y al tópico `/rosout`.

- **Niveles de Gravedad:** `DEBUG`, `INFO`, `WARN`, `ERROR` y `FATAL`.
- **Uso en Python:** Se accede a través de `self.get_logger().info("Mensaje")`. El logger incluye automáticamente el nombre del nodo y el espacio de nombres.

## 5. Compilación y Ejecución

Una vez escrito el código, el paquete debe ser procesado por el sistema de construcción de ROS 2.

### Herramienta `colcon`

`colcon` es la herramienta de línea de comandos utilizada para construir paquetes.

1. **Compilación:** Desde la raíz del workspace, se ejecuta:
2. **Actualización del Entorno:** Tras compilar, se debe volver a hacer source del archivo local para que el nuevo nodo sea rastreable:

### Ejecución del Nodo

Para iniciar el nodo, se utiliza el comando `ros2 run`:

```bash
ros2 run <nombre_del_paquete> <nombre_del_ejecutable>
```

## Resumen de Comandos de Terminal Necesarios

|                      |                                                           |
| -------------------- | --------------------------------------------------------- |
| Acción               | Comando                                                   |
| Crear Workspace      | `mkdir -p ~/ros2_ws/src`                                  |
| Crear Paquete        | `ros2 pkg create --build-type ament_python comms_basicas` |
| Compilar             | `colcon build`                                            |
| Configurar Entorno   | `source install/local_setup.bash`                         |
| Ejecutar Nodo        | `ros2 run comms_basicas generador_pulsos`                 |
| Listar Nodos Activos | `ros2 node list`                                          |
| Ver Info de Nodo     | `ros2 node info /<nombre_del_nodo>`                       |

# Guía Teórico-Práctica: Gestión de Parámetros en ROS 2 con Python

En el ecosistema de ROS 2 (Robot Operating System), la capacidad de configurar y ajustar el comportamiento de los nodos sin necesidad de recompilar el código es fundamental. Esta funcionalidad se logra a través de los **parámetros**, los cuales actúan como variables de configuración globales o locales para un nodo específico.

## 1. Concepto de Parámetros

Los parámetros son esencialmente ajustes de configuración de un nodo. Pueden considerarse como el equivalente a variables de configuración que permiten alterar el funcionamiento de un algoritmo, definir límites de velocidad o especificar puertos de comunicación en tiempo de ejecución.

### Tipos de Datos Soportados

ROS 2 utiliza un sistema de tipos estrictos basado en IDL (Interface Definition Language). Los parámetros en `rclpy` (la biblioteca cliente de Python) soportan los siguientes tipos de datos básicos y sus versiones en arreglos:

|   |   |
|---|---|
|Tipo de Dato|Descripción|
|**Booleanos**|Valores `true` o `false`.|
|**Enteros**|Números enteros (int64).|
|**Floats**|Números de punto flotante (double/float64).|
|**Strings**|Cadenas de caracteres de texto.|
|**Arreglos**|Listas de cualquiera de los tipos anteriores (ej. arreglos de enteros o strings).|

--------------------------------------------------------------------------------

## 2. Declaración de Parámetros en Python (rclpy)

Para que un parámetro sea accesible y pueda ser modificado externamente, debe ser registrado formalmente dentro del constructor del nodo. En ROS 2, no basta con definir una variable interna; es obligatorio utilizar el método `declare_parameter`.

### El método `declare_parameter`

Este método registra el parámetro en la interfaz del nodo y le asigna un valor por defecto. Su sintaxis básica es:

```python
self.declare_parameter('nombre_del_parametro', valor_por_defecto)
```

**Ejemplo de implementación en un nodo:** Si se desea configurar la frecuencia de un ciclo de control (por ejemplo, a 10 Hz por defecto), el código dentro de la clase del nodo sería:

```python
import rclpy
from rclpy.node import Node

class MiNodoConfigurable(Node):
    def __init__(self):
        super().__init__('mi_nodo_configurable')
        # Declaración obligatoria del parámetro
        self.declare_parameter('frecuencia_control', 10.0)
```

--------------------------------------------------------------------------------

## 3. Lectura de Parámetros desde el Código

Una vez declarado, el nodo puede acceder al valor actual del parámetro en cualquier momento utilizando el método `get_parameter`. Es importante notar que este método devuelve un objeto de tipo `Parameter`, por lo que se debe extraer su propiedad `.value`.

### Uso de `get_parameter`

Para obtener el valor real y asignarlo a una variable interna:

```python
# Obtener el objeto parámetro
param_obj = self.get_parameter('frecuencia_control')

# Extraer el valor real (float, int, etc.)
frecuencia = param_obj.value

# Ejemplo de uso: crear un timer con esa frecuencia
self.timer = self.create_timer(1.0 / frecuencia, self.timer_callback)
```

--------------------------------------------------------------------------------

## 4. Inyección de Parámetros desde la Terminal

Una de las grandes ventajas de ROS 2 es la posibilidad de sobrescribir los valores definidos en el código al momento de arrancar el nodo, utilizando argumentos de línea de comandos.

### Sintaxis `--ros-args -p`

Al utilizar el comando `ros2 run`, se deben emplear los flags específicos de ROS para pasar parámetros. El formato es:

```bash
ros2 run nombre_paquete nombre_ejecutable --ros-args -p parametro:=valor
```

**Ejemplo práctico:** Si queremos arrancar el nodo anterior pero con una frecuencia de 20 Hz en lugar de los 10 Hz definidos por defecto:

```bash
ros2 run mi_paquete mi_nodo_script --ros-args -p frecuencia_control:=20.0
```

--------------------------------------------------------------------------------

## 5. Interacción en Vivo (CLI)

ROS 2 proporciona herramientas de introspección para inspeccionar y alterar variables mientras el nodo ya se encuentra en ejecución (runtime), sin necesidad de reiniciarlo.

### Comandos de Consola Esenciales

- **Listar parámetros:** Muestra todos los parámetros registrados por los nodos activos.
- **Obtener valor actual:** Consulta el valor de un parámetro específico de un nodo.
- **Modificar en tiempo real:** Cambia el valor de un parámetro mientras el nodo corre.

--------------------------------------------------------------------------------

## 6. Archivos de Configuración (YAML)

Cuando un sistema robótico posee decenas de parámetros, resulta ineficiente pasarlos uno a uno por la terminal. ROS 2 permite agrupar estas configuraciones en archivos `.yaml`.

### Estructura del archivo YAML

El archivo debe seguir una jerarquía que especifique el nombre del nodo y luego sus parámetros:

```yaml
mi_nodo_configurable:
  ros__parameters:
    frecuencia_control: 15.0
    modo_seguro: true
    nombre_robot: "Tiago"
```

### Carga mediante `--params-file`

Para iniciar un nodo cargando todos los valores desde el archivo:

```bash
ros2 run mi_paquete mi_nodo_script --ros-args --params-file ruta/al/archivo.yaml
```

--------------------------------------------------------------------------------

## 7. Callbacks de Parámetros: Actualización Dinámica

Para que un nodo reaccione inmediatamente cuando alguien cambia un parámetro (por ejemplo, mediante `ros2 param set`), se deben registrar **callbacks**. Sin estos métodos, el código solo leería el valor al inicio y no se enteraría de los cambios posteriores.

### Métodos de Reacción en Tiempo Real

En Python, se utiliza el método `add_on_set_parameters_callback` para registrar una función que se ejecute cada vez que un parámetro sea alterado.

**Ejemplo de lógica de un Callback:**

```python
from rcl_interfaces.msg import SetParametersResult

class MiNodoDinamico(Node):
    def __init__(self):
        super().__init__('mi_nodo_dinamico')
        self.declare_parameter('limite_velocidad', 0.5)
        # Registrar el callback
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'limite_velocidad' and param.type_ == param.Type.DOUBLE:
                self.get_logger().info(f'Nuevo límite de velocidad: {param.value}')
                # Aquí se podrían ejecutar acciones como actualizar controladores
        
        return SetParametersResult(successful=True)
```

Este mecanismo garantiza que el nodo sea verdaderamente dinámico, permitiendo ajustes finos durante la operación del robot sin interrupciones en el flujo de ejecución.
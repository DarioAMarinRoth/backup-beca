# Guía Práctica: Fundamentos de ROS 2 en Python para Integración de Hardware

Esta guía está diseñada para desarrollar las competencias estrictamente necesarias para encapsular una comunicación serie/Modbus dentro de la arquitectura de ROS 2.

## Ejercicio 1: El Esqueleto y el Tiempo Real

**Consigna:**

1. Crea un _workspace_ de ROS 2 y un paquete llamado `comms_basicas` usando `ament_python`.
    
2. Escribe un nodo llamado `generador_pulsos`.
    
3. Configura un _Timer_ dentro del nodo que imprima en consola (usando `self.get_logger().info()`) el mensaje "Leyendo hardware..." exactamente cada 0.5 segundos.
    
4. Compila el paquete con `colcon` y ejecuta el nodo.
    

**Objetivo del ejercicio:**

Aprender la estructura de directorios de ROS 2, el proceso de compilación (`colcon build`) y el uso de _Timers_. El uso de Timers es imperativo en hardware: te enseña a ejecutar tareas periódicas (como leer registros Modbus) de forma no bloqueante, permitiendo que el nodo escuche otras instrucciones simultáneamente.

## Ejercicio 2: Flujo Continuo de Datos (Telemetría y Setpoints)

**Consigna:**

1. Modifica el paquete anterior para incluir dos nodos distintos: `sensor_falso` y `monitor`.
    
2. `sensor_falso`: Publica un número decimal aleatorio entre 0.0 y 24.0 (usando el tipo de mensaje estándar `std_msgs/msg/Float32`) en el topic `/voltaje_bateria` a una frecuencia de 10 Hz.
    
3. `monitor`: Se suscribe al topic `/voltaje_bateria` y cada vez que recibe un dato, imprime en consola: "Voltaje recibido: X.XX V".
    

**Objetivo del ejercicio:**

Dominar el patrón Publicador/Suscriptor (Topics). Este es el mecanismo exacto que utilizarás para extraer los floats de 32 bits de las baterías/motores desde el STM32 y ponerlos a disposición de toda la red, y viceversa, para recibir los setpoints de movimiento.

## Ejercicio 3: Órdenes Críticas y Confirmación

**Consigna:**

1. Crea un nodo llamado `gestor_energia`.
    
2. Implementa un Servidor (Service Server) en este nodo para el servicio `/interruptor_principal`. Utiliza el tipo de servicio estándar `std_srvs/srv/SetBool`.
    
3. Si el servicio recibe `True`, el nodo debe imprimir "Sistema ARMADO" y devolver un mensaje de éxito (`success=True`, `message="Armado completado"`). Si recibe `False`, imprime "Sistema DESARMADO" y devuelve éxito.
    
4. Llama a este servicio desde la terminal usando la CLI de ROS 2 (`ros2 service call ...`).
    

**Objetivo del ejercicio:**

Diferenciar entre flujos continuos (Topics) y operaciones síncronas de Petición/Respuesta (Services). Entenderás cómo enviar comandos de estado crítico (Armado/Desarmado) que requieren confirmación de ejecución antes de que el sistema continúe.

## Ejercicio 4: Configuración Dinámica

**Consigna:**

1. Toma el nodo `sensor_falso` del Ejercicio 2 y declárale dos parámetros: `puerto_com` (tipo string, valor por defecto "/dev/ttyUSB0") y `frecuencia_hz` (tipo double, valor por defecto 10.0).
    
2. Haz que el _Timer_ del nodo ajuste su tiempo de ejecución dinámicamente basado en el parámetro `frecuencia_hz`.
    
3. Haz que en la inicialización, el nodo imprima: "Conectando al puerto: [valor_de_puerto_com]".
    
4. Ejecuta el nodo cambiando estos parámetros desde la línea de comandos al momento de lanzarlo, sin modificar el código Python.
    

**Objetivo del ejercicio:**

Utilizar el servidor de Parámetros de ROS 2. Esto es fundamental para tu script Modbus: te permitirá cambiar el puerto serie, el baudrate o el Slave ID del STM32 dependiendo de la computadora o configuración del robot sin tener que editar el código fuente ni recompilar.

## Ejercicio 5: Empaquetado de Datos

**Consigna:**

1. Crea un paquete nuevo llamado `mis_interfaces` del tipo `ament_cmake` (los mensajes personalizados requieren CMake, aunque uses Python en los nodos).
    
2. Crea un archivo `EstadoMotor.msg` que contenga tres campos: `float32 rpm`, `float32 corriente_a`, y `float32 temperatura_c`.
    
3. Modifica tu nodo compilado en el Ejercicio 2 para que ahora publique y se suscriba utilizando este nuevo mensaje `EstadoMotor` en lugar de un `Float32` simple.
    

**Objetivo del ejercicio:**

Crear _Custom Interfaces_. Cuando leas múltiples registros de 16 bits vía Modbus y los conviertas a floats, no querrás enviarlos por separado. Este ejercicio te enseña a empaquetar variables relacionadas en un solo mensaje estructurado, optimizando el ancho de banda y manteniendo la coherencia de los datos del STM32.
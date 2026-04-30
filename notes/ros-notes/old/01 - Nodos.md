
Cada [[Computación distribuida y networking#^c70871|nodo]] en ROS debe ser responsable de una sola tarea modular. Cada nodo puede enviar o recibir datos a través de [[02 - Topics|topics]], [[servicios|servicios]], [[acciones|acciones]] o [[parámetros|parámetros]].

## Tasks
### `ros2 run`

Para correr un ejecutable de un paquete se utiliza el comando `ros2 run`.

```shell
ros2 run <package_name> <executable_name>
```

> [!example]
> En el siguiente comando:
> ```shell
> ros2 run turtlesim turtlesim_node
> ```
> El nombre del paquete es `turtlesim` y el nombre del ejecutable es `turtlesim_node`.

### `ros2 node list`

Para saber los nombres de todos los nodos que se están ejecutando se utiliza el comando `ros2 node list`.

> [!Example]
> Si se ejecuta el [[#^bb33b9|comando anterior]] y luego se listan los nodos con `ros2 node list` debería verse algo tal que asi:
> ```shell
> ros2 node list
> /turtlesim
> ```

### Remapping

El remapeo permite reasignar las propiedades por defecto de los nodos (el nombre, el nombre del topic, el nombre de los servicios, etc.) a valores custom.

> [!Example]
>  El siguiente ejemplo cambia el nombre del nodo a uno personalizado:
>  ```shell
>  ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle
>  ```
>  El flag `--ros-args` sirve para delimitar los argumentos del ejecutable con los de ros.

### `ros2 node info`

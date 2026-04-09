# Construcción del entorno

## Procedimiento

Posicionados en la carpeta `src`
```shell
ros2 pkg create --build-type ament_python my_first_pkg
```
Después desde la carpeta `chacras_ws`:

```
colcon build
source install/setup.bash
```

### Notas

`chacras_ws` es un workspace. Un workspace es simplemente un directorio que contiene paquetes de ros. Un paquete es una unidad que contiene código de ros. Para que los paquetes de un workspace estén disponibles en la terminal es necesario hacer `source` al workspace.

Existe algo denominado el _underlay_ que es como un workspace base sobre el cual se apoya el propio workspace. Normalmente es el que ya instalamos y contiene los paquetes oficiales de ROS.

Por otro lado el _overlay_ es un workspace custom que se crea por encima del _underlay_ para hacer nuestros propios paquetes. Por lo tanto, básicamente `chacras_ws` es un overlay sobre el underlay.

> [!NOTE]
> ros busca primero los paquetes en el overlay, si no los encuentra revisa el underlay.

El comando `ros2 pkg create` crea un paquete. Para crear un paquete se usa ament como build system y colcon como build tool. La sintaxis para crear un paquete usando python es:

```shell
ros2 pkg create --build-type ament_python <package_name>
```

Para buildear el paquete hay dos alternativas:

Para hacer build a todos los paquetes del workspace
```shell
colcon build
```

Para hacer build solo a paquetes específicos:

```
colcon build --packages-select <package_name>
```

Por último, hay que hacer source a la instalación de ros:

```shell
source install/local_setup.bash
```



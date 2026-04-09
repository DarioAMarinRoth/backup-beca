
ROS 2 utiliza el entorno de shell para trabajar en combinación con workspaces. Específicamente utiliza las variables de entorno del shell para determinar dónde buscar paquetes, ejecutables y librerías. Cada workspace tiene un archivo `setup.bash` que, al ser ejecutado modifica las variables de entorno, agregando las rutas específicas de ese workspace.

El underlay establece las rutas fundamentales del sistema. Los overlays se superponen al underlay modificando las mismas variables de entorno, pero anteponiéndose en el orden de búsqueda.

## Instalación

https://docs.ros.org/en/kilted/Installation/Ubuntu-Install-Debs.html

## Tareas

### Cargar configuración de ROS

Para acceder a los comandos de ROS 2 hay que ejecutar el siguiente comando en cada nueva shell que se abra:
```shell
source /opt/ros/kilted/setup.bash
```

> [!note]
> Como estoy usando fish como shell, no puedo correr ese script directamente. Instalé un plugin para fish que se llama `bass` que me permite ejecutar comandos de bash.
> Para ejecutar cualquier comando de bash, solamente hay que anteponer `bass` al comando.

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

### Verificar las variables de entorno

Cargar la configuración de ROS configurará varias variables de entorno que necesita para funcionar. Para saber si están cargadas correctamente se pueden verificar con el siguiente comando:
```shell
printenv | grep -i ROS
```

De el output que arroje deberíamos verificar que las variables `ROS_DISTRO` y `ROS_VERSION` estén cargadas:
```bash
ROS_VERSION=2
ROS_PYTHON_VERSION=3
ROS_DISTRO=kilted
```

### `ROS_DOMAIN_ID`

ROS 2 utiliza [[Computación distribuida y networking#DDS|DDS]] (Data Distribution Service) como middleware predeterminado para la comunicación.
Por defecto, el [[Computación distribuida y networking#El Domain ID|domain ID]] de los [[Computación distribuida y networking#^c70871|nodos]] es 0. Para  evitar interferencia entre distintos grupos de nodos conviene asignar un ID diferente a cada grupo.
La forma fácil, rápida y segura es asignar un ID entre 0 y 101 inclusive. Hay un [artículo](https://docs.ros.org/en/kilted/Concepts/Intermediate/About-Domain-ID.html) en explica una forma más larga de asignar el ID.
Una vez elegido el domain_id se puede configurar la variable de entorno correspondiente con el siguiente comando:

```shell
export ROS_DOMAIN_ID=<your_domain_id>
```

Adicionalmente, para mantener la configuración entre las sesiones de shell, se puede añadir el siguiente comando al script de start de la shell:
```shell
echo "export ROS_DOMAIN_ID=<your_domain_id>" >> ~/.bashrc
```

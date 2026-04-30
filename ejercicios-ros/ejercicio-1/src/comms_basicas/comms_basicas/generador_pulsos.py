import rclpy
from rclpy.node import Node

class GeneradorPulsos(Node):

    def __init__(self, node_name):
        super().__init__(node_name)
        self.create_timer(0.5, self.log)

    def log(self):
        self.get_logger().info("Leyendo hardware")


def main() -> None:
    rclpy.init()
    generador_pulsos = GeneradorPulsos("generador_pulsos")
    rclpy.spin(generador_pulsos)
    generador_pulsos.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

import rclpy
import random

from rclpy.node import Node
from std_msgs.msg import Float32


class Sensor(Node):
    
    def __init__(self, node_name):
        super().__init__(node_name)
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("freq_hz",10)
        qos = 10
        self._publisher = self.create_publisher(Float32, "/voltaje_bateria", qos)
        freq = self.get_parameter("freq_hz").value
        self._period = 1 / freq
        self.create_timer(self._period, self.publish)
        self.get_logger().info(f"Conectando al puerto {self.get_parameter('port').value}")

    def publish(self):
        msg = Float32()
        msg.data = round(random.random() * 24, 1)
        self._publisher.publish(msg)

def main() -> None:
    rclpy.init()
    sensor = Sensor("sensor_falso")
    rclpy.spin(sensor)
    sensor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
import rclpy
import random

from rclpy.node import Node
from my_interfaces.msg import MotorStatus



class Motor(Node):

    def __init__(self, node_name, freq=10):
        super().__init__(node_name)
        qos = 10
        self._period = 1 / freq
        self._publisher = self.create_publisher(MotorStatus, "/motor", qos)
        self.create_timer(self._period, self.publish)

    def publish(self):
        msg = MotorStatus()
        msg.rpm = round(random.random() * 240, 1)
        msg.corriente_a = round(random.random() * 3 , 1)
        msg.temperatura_c = round(random.random() * 10  + 18, 1)
        self._publisher.publish(msg)


def main() -> None:
    rclpy.init()
    motor = Motor("motor")
    rclpy.spin(motor)
    motor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

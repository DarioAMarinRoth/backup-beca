import rclpy
from rclpy.node import Node
from my_interfaces.msg import MotorStatus

class Monitor(Node):

    def __init__(self, node_name):
        super().__init__(node_name)
        qos = 10
        self.create_subscription(MotorStatus, "/motor", self.log_voltage, qos)

    def log_voltage(self, msg):
        print("Mensaje recibido")
        print(f"RPM: {msg.rpm:.2f}")
        print(f"Corriente [A]: {msg.corriente_a:.2f}")
        print(f"Temperatura [C]: {msg.temperatura_c:.2f}")

def main() -> None:
    rclpy.init()
    monitor = Monitor("monitor")
    rclpy.spin(monitor)
    monitor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
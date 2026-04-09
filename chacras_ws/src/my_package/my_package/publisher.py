import rclpy # rclpy provides the canonical Python API for interacting with ROS 2.
from rclpy.node import Node # Clase Node, necesaria para crear nodos
from std_msgs.msg import String 

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'chatter', 10) # Docs: https://docs.ros.org/en/iron/p/rclpy/api/topics.html#module-rclpy.publisher
        timer_period = 1.0  # segundos
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hola desde ROS 2!'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
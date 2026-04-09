import rclpy
from rclpy.node import Node
from modbus_demo.srv import ReadRegister, WriteRegister
from modbus_demo.modbus.connector import ModbusConnector

class ModbusProvider(Node):

    def __init__(self):
        super().__init__('modbus_provider')
        self.modbus = ModbusConnector()
        self.read_service = self.create_service(ReadRegister, 'read_register', self.read_callback)
        self.write_service = self.create_service(WriteRegister, 'write_register', self.write_callback)
        self.get_logger().info('Modbus Provider is ready to handle requests.')

    def read_callback(self, request, response):
        data = self.modbus.get(request.address, request.count)
        if data is None:
            response.error = 1
            response.values = []
        else:
            response.error = 0
            response.values = data
        return response
    
    def write_callback(self, request, response):
        success = self.modbus.set(request.address, request.values)
        response.error = 0 if success else 1
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ModbusProvider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
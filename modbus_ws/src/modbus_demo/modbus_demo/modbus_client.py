from modbus_demo.modbus_demo.modbus.modbus_regs import ModbusRegs
import rclpy
from rclpy.node import Node
from modbus_demo.srv import ReadRegister

class ModbusClient(Node):
    
    def __init__(self):
        super().__init__('modbus_client')
        self.client = self.create_client(ReadRegister, 'read_register')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando servicio...')
        self.timer = self.create_timer(2.0, self.call_service)

    def call_service(self):
        req = ReadRegister.Request()
        req.address = ModbusRegs.ARMADO_SISTEMA
        req.count = 1

        future = self.client.call_async(req)
        future.add_done_callback(self.response_callback)
    
    def response_callback(self, future):
        result = future.result()
        if result.error == 0:
            self.get_logger().info(f"Valor leído: {result.values}")
        else:
            self.get_logger().error("Error leyendo registro")

def main(args=None):
    rclpy.init(args=args)
    node = ModbusClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
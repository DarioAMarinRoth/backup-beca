import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class PowerManager(Node):

    _POWER_ON = False

    def __init__(self, node_name):
        super().__init__(node_name)
        self.create_service(SetBool, "/master_switch", self.set_power)

    
    def set_power(self, request, response):
        
        response.success = False

        PowerManager._POWER_ON = request.data
        
        if PowerManager._POWER_ON:
            self.get_logger().info("SISTEMA ARMADO")
            response.success = True
            response.message = "Armado completado"
        else:
            self.get_logger().info("SISTEMA DESARMADO")
            response.success = True
            response.message = "Desarmado completado"
        return response
        

def main() -> None:
    rclpy.init()
    power_manager = PowerManager("power_manager")
    rclpy.spin(power_manager)
    power_manager.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

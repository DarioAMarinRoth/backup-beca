from pymodbus.client import ModbusSerialClient


class ModbusConnector:

    def __init__(self):
        self.client = ModbusSerialClient(
            port='/dev/ttyUSB0',
            baudrate=115200,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )

    def connect(self):
        if not self.client.connect():
            print("Error :(")
            exit(1)
        print("Conectado")

    def set(self, address, value, slave=1):
        result = self.client.write_register(address=address, value=value, slave=slave)
        if result.isError():
            return False
        return True

    def get(self, address, count=1, slave=1):
        data = self.client.read_holding_registers(address=address, count=count, slave=slave)         
        if data.isError():
            # TODO: lanzar excepciones 
            return None
        return data.registers


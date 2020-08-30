from pymodbus.client.sync import ModbusTcpClient as ModbusClient

class BlowerInverter:
    def __init__(self, host: str, port: int) -> None:
        self.client = ModbusClient(host=host, port=port)
        status = self.client.connect()
        if status == False:
            raise Exception("Could not connect to the tcp server")

    def read_register(self, address):
        return self.client.read_holding_registers(address, count=1, unit=0).registers

    def write_register(self, address, value):
        return self.client.write_register(address, value, unit=0).registers

    def write_registers(self, address, values):
        return self.client.write_registers(address, values, unit=0).registers

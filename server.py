from opcua import Server
import time
from datetime import datetime
from device import Device

class OPCUAServer:
    '''
    Class that represents an OPC UA server hosting multiple virtual devices.
    '''
    def __init__(self, endpoint="opc.tcp://localhost:4840/freeopcua/server/"):
        self.server = Server()
        self.server.set_endpoint(endpoint)

        uri = "http://opc-ua-playground.org/example/"
        self.idx = self.server.register_namespace(uri)
        self.devices = []

    def add_device(self, name):
        '''Add a new virtual device to the server.'''
        device = Device(self.server, self.idx, name)
        self.devices.append(device)
        print(f"Added device: {name}")
        return device
    
    def start(self):
        '''Start the OPC UA server and update device variables periodically.'''
        self.server.start()
        print(f"OPC UA Server started at {self.server.endpoint.geturl()}")
        print("Press Ctrl+C to stop the server.\n")

        try:
            while True:
                for device in self.devices:
                    device.update_variables()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}]\n"
                          f"{device.name} -> T={device.temperature.get_value()} °C, "
                          f"P={device.pressure.get_value()} bar, "
                          f"Running={device.running.get_value()}")
                time.sleep(2)
        except KeyboardInterrupt:
            print("Shutting down server manually...")
        finally:
            self.server.stop()
            print("Server stopped.")

if __name__ == "__main__":
    opc_server = OPCUAServer()
    opc_server.add_device("Boiler_1")
    opc_server.add_device("Pump_2")
    opc_server.start()
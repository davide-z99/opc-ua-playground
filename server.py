from opcua import Server
import random
import time
from datetime import datetime

class Device:
    '''
    Class that represents a virtual OPC UA device
    with some variables(temperature, pressure, running).
    '''
    def __init__(self, server, idx, name):
        self.name = name
        self.device_node = server.get_objects_node().add_object(idx, name)

        # Simulated variables
        self.temperature = self.device_node.add_variable(idx, "Temperature", 20.0)
        self.pressure = self.device_node.add_variable(idx, "Pressure", 1.02)
        self.running = self.device_node.add_variable(idx, "Running", False)

        # Set variables to be writable by clients
        for var in [self.temperature, self.pressure, self.running]:
            var.set_writable()
    
    def update_variables(self):
        '''Periodically update the device variables with random values.'''
        temp = self.temperature.get_value() + random.uniform(-0.5, 0.5)
        pres = self.pressure.get_value() + random.uniform(-0.01, 0.01)
        self.temperature.set_value(round(temp, 2))
        self.pressure.set_value(round(pres, 3))
        self.running.set_value(random.choice([True, False]))

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
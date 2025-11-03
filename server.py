from opcua import Server, ua
import random
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Data Model Classes
class SensorData:
    """
    Container for a sensor reading with metadata.
    """
    def __init__(self, value, unit="N/A", quality="Good"):
        self.value = value
        self.unit = unit
        self.quality = quality
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"SensorData (value={self.value}, unit='{self.unit}', quality='{self.quality}', timestamp='{self.timestamp:%H:%M:%S}')"
        

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
        
        # Reset method
        self.device_node.add_method(idx, "ResetDevice", self.reset_device, [], [ua.VariantType.Boolean])
        logging.info(f"Device '{self.name}' registerd with variables and ResetDevice method.")

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
        logging.info(f"Device '{self.name}' updated: T={temp:.2f}, P={pres:.3f}, Running={self.running.get_value()}")

    def reset_device(self):
        """Reset device variables to default values (Called via OPC UA method)."""
        print(f"Resetting device '{self.name}' to default values...")
        self.temperature.set_value(20.0)
        self.pressure.set_value(1.02)
        self.running.set_value(False)
        logging.info(f"Device '{self.name}' has been reset to default values.")
        return True

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
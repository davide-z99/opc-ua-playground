from opcua import Client, ua
import time

class OPCUARequestClient:
    def __init__(self, endpoint="opc.tcp://localhost:4840/freeopcua/server/"):
        self.client = Client(endpoint)
        self.devices = []

    def connect(self):
        print(f"Connecting to {self.client.server_url.geturl()} ...")
        self.client.connect()
        print("Connected to OPC UA Server\n")

    def browse_devices(self):
        print("Browsing devices...")
        objects = self.client.get_objects_node()
        for node in objects.get_children():
            browse_name = node.get_browse_name().Name
            if "Device" in browse_name or "Boiler" in browse_name or "Pump" in browse_name:
                self.devices.append(node)
                print(f"  • Found device: {browse_name}")
        print()

    def read_variable(self, device_name, variable_name):
        device_node = next((d for d in self.devices if device_name in d.get_browse_name().Name), None)
        if not device_node:
            print(f"Device '{device_name}' not found.")
            return None

        for var in device_node.get_children():
            if variable_name in var.get_browse_name().Name:
                value = var.get_value()
                print(f"{device_name}.{variable_name} = {value}")
                return value

        print(f"Variable '{variable_name}' not found in {device_name}.")
        return None

    def write_variable(self, device_name, variable_name, new_value):
        device_node = next((d for d in self.devices if device_name in d.get_browse_name().Name), None)
        if not device_node:
            print(f"Device '{device_name}' not found.")
            return False

        for var in device_node.get_children():
            if variable_name in var.get_browse_name().Name:
                var.set_value(new_value)
                print(f"{device_name}.{variable_name} set to {new_value}")
                return True

        print(f"Variable '{variable_name}' not found in {device_name}.")
        return False

    def call_method(self, device_name, method_name):
        device_node = next((d for d in self.devices if device_name in d.get_browse_name().Name), None)
        if not device_node:
            print(f"Device '{device_name}' not found.")
            return

        for child in device_node.get_children():
            if method_name in child.get_browse_name().Name:
                print(f"Calling {device_name}.{method_name}() ...")
                self.client.uaclient.call(child)
                print("Method executed.")
                return
        print(f"Method '{method_name}' not found in {device_name}.")

    def disconnect(self):
        self.client.disconnect()
        print("\nDisconnected from OPC UA Server")


if __name__ == "__main__":
    client = OPCUARequestClient()
    try:
        client.connect()
        client.browse_devices()

        client.read_variable("Pump_2", "Temperature")
        client.read_variable("Pump_2", "Pressure")
        client.read_variable("Pump_2", "Running")
        client.call_method("Pump_2", "ResetDevice")

        time.sleep(1)

    finally:
        client.disconnect()

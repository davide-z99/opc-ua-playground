from opcua import Client, ua
import time
import logging

# Configure logging
logging.basicConfig(
    filename="logs/client.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Callback Handler
class SubHandler:
    """
    Handles data change events from the OPC UA server.
    """

    def __init__(self, node_names):
        self.node_names = node_names
            
    def datachange_notification(self, node, val, data):
        name = self.node_names.get(node.nodeid, "Unknown")
        logging.info(f"Data change on {name}: {val}")
        print(f"Data change on {name}: {val}")

    def event_notification(self, event):
        logging.info(f"New event: {event}")        

class OPCUAClient:
    def __init__(self, url):
        self.url = url
        self.client = Client(url)
        self.sub = None
        self.handler = None

    def connect(self):
        self.client.connect()
        logging.info(f"Connected to OPC UA Server at {self.url}")
        print(f"Connected to OPC UA Server at {self.url}")

    def browse(self):
        '''Print server's nodes structure'''
        
        objects = self.client.get_objects_node()
        device_nodes = []

        for device in objects.get_children():
            name = device.get_browse_name().Name
            print(f"Found device: {name}")
            logging.info(f"Found device: {name}")
            device_nodes.append(device)

            for var in device.get_children():
                if var.get_node_class() == ua.NodeClass.Variable:
                    var_name = var.get_browse_name().Name
                    var_value = var.get_value()
                    print(f" - {var_name}: {var_value}")
                else:
                    # Not a variable node
                    var_name = var.get_browse_name().Name
                    print(f" - {var_name}: <Not a variable node>")
            print("")
    
    def monitor(self, interval):
        '''
        Continuously monitor device variables
        '''
        print("\nStarting live monitoring...\n")
        object = self.client.get_objects_node()
        devices = object.get_children()
        try:
            while True:
                for dev in devices:
                    # Filter only custom devices (namespace index 2)
                    if dev.nodeid.NamespaceIndex != 2:
                        continue
                    
                    dev_name = dev.get_browse_name().Name
                    print(f"Device: {dev_name}")

                    for var in dev.get_children():
                        try:
                            # Only read variable nodes
                            if var.get_node_class() == ua.NodeClass.Variable:
                                var_name = var.get_browse_name().Name
                                var_value = var.get_value()
                                print(f"{var_name} -> {var_value}")
                            else:
                                continue
                        except Exception as e:
                            # Ignore unreadable or temporary nodes
                            print(f"Error reading device {dev_name}: {e}")
                            continue

                    print("")

                time.sleep(interval)
                print("-" * 40)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")


    def reset_device(self, device):
        """Call the ResetDevice OPC UA method remotely on the specified device."""
        methods = [child for child in device.get_children() if "ResetDevice" in child.get_browse_name().Name]
        if methods:
            logging.info(f"Calling ResetDevice method on {device.get_browse_name().Name}")
            device.call_method(methods[0])
            print(f"ResetDevice method called on {device.get_browse_name().Name}")
    
    def disconnect(self):
        self.client.disconnect()
        logging.info("Disconnected from OPC UA Server")
        print("Disconnected from OPC UA Server")

if __name__ == "__main__":
    client = OPCUAClient("opc.tcp://localhost:4840/freeopcua/server/")
    client.connect()
    devices = client.browse()

    if client.browse():
        client.reset_device(devices[0])
    
    try:
        client.monitor(interval = 2)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
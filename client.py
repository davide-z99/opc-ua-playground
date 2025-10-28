from opcua import Client, ua
import time

class OPCUAClient:
    def __init__(self, url):
        self.url = url
        self.client = Client(url)

    def connect(self):
        self.client.connect()
        print(f"Connected to OPC UA Server at {self.url}")

    def browse(self):
        '''Print server's nodes structure'''
        objects = self.client.get_objects_node()
        for device in objects.get_children():
            name = device.get_browse_name().Name
            print(f"Found device: {name}")
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


    def disconnect(self):
        self.client.disconnect()
        print("Disconnected from OPC UA Server")

if __name__ == "__main__":
    client = OPCUAClient("opc.tcp://localhost:4840/freeopcua/server/")
    client.connect()
    client.browse()
    try:
        client.monitor(interval = 2)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
from opcua import Client, ua
from sub_handler import SubHandler
import time

class OPCUAClient:
    def __init__(self, url):
        self.url = url
        self.client = Client(url)
        self.sub = None
        self.handler = None

    def connect(self):
        print(f"Connecting to OPC UA Server at {self.url}...")
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

    def subscribe_to_device(self, device_name):
        """
        Subscribe to all variable nodes of a given device
        """
        objects_node = self.client.get_objects_node()
        device_node = None

        # Find the device node by name
        for dev in objects_node.get_children():
            if dev.get_browse_name().Name == device_name:
                device_node = dev
                break

        if not device_node:
            print(f"Device '{device_name}' not found on server.")
            return
        
        print(f"Subscribing to device: {device_name}")
        handler = SubHandler()
        self.sub = self.client.create_subscription(500, handler)

        for var in device_node.get_children():
            # Subscribe only to variable nodes
            try:
                _ = var.get_value()  # Test if readable
                name = var.get_browse_name().Name
                handler.node_names[var.nodeid.to_string()] = name
                self.sub.subscribe_data_change(var)
                print(f"   → Subscribed to {name}")
            except Exception:
                pass
    
    # def monitor(self, interval):
    #     '''
    #     Continuously monitor device variables
    #     '''
    #     print("\nStarting live monitoring...\n")
    #     object = self.client.get_objects_node()
    #     devices = object.get_children()
    #     try:
    #         while True:
    #             for dev in devices:
    #                 # Filter only custom devices (namespace index 2)
    #                 if dev.nodeid.NamespaceIndex != 2:
    #                     continue
                    
    #                 dev_name = dev.get_browse_name().Name
    #                 print(f"Device: {dev_name}")

    #                 for var in dev.get_children():
    #                     try:
    #                         # Only read variable nodes
    #                         if var.get_node_class() == ua.NodeClass.Variable:
    #                             var_name = var.get_browse_name().Name
    #                             var_value = var.get_value()
    #                             print(f"{var_name} -> {var_value}")
    #                         else:
    #                             continue
    #                     except Exception as e:
    #                         # Ignore unreadable or temporary nodes
    #                         print(f"Error reading device {dev_name}: {e}")
    #                         continue

    #                 print("")

    #             time.sleep(interval)
    #             print("-" * 40)
    #     except KeyboardInterrupt:
    #         print("\nMonitoring stopped by user.")


    def disconnect(self):
        print("Disconnecting from OPC UA Server...")
        if self.sub:
            self.sub.delete()
        self.client.disconnect()
        print("Disconnected from OPC UA Server")

if __name__ == "__main__":
    client = OPCUAClient("opc.tcp://localhost:4840/freeopcua/server/")
    client.connect()
    client.browse()
    client.subscribe_to_device("Boiler_1")
    try:
        #client.monitor(interval = 2)
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
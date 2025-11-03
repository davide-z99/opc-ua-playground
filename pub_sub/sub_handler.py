class SubHandler:
    """
    Handles data change events from the OPC UA server
    """
    def __init__(self):
        self.node_names = {}

    def datachange_notification(self, node, val, data):
        try:
            nodeid = node.nodeid.to_string()
            name = self.node_names.get(nodeid, nodeid)
            print(f"Data Change on {name}: \nNew Value = {val}")
        except Exception as e:
            print(f"Error in datachange_notification: {e}")

    def event_notification(self, event):
        print(f"New Event: {event}")
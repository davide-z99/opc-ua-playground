import random

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
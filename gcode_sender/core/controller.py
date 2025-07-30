import time
from .serialBridge import SerialBridge
from .commandIterator import SweepCommandIterator
from .gcode_file import ExampleGcodeFile
import events

MAX_BUFFER_SIZE = 5

"""
TODO
"""
class Controller:
    SERIAL_TIMEOUT = 1 # seconds
    MAX_TEMP_OFFSET = 5 # degrees celcius

    def __init__(self, logger):
        self.logger = logger
        self.commandIterator = SweepCommandIterator()
        self.serialBridge = SerialBridge()
        self.aprox_buffer = 0 # an estimate of the current planner buffer size in the arduino
        # this is a theoretical maximum

        self.gcode_file = ExampleGcodeFile()
        self.register_event(events.NewGcodeFileHandler())

        self.target_temperature = 20
    
    def connect(self):
        self.serialBridge.connect()
        # initialize (wait for Grbl line)
        while "Grbl" not in self.serialBridge.readline():
            ...
        #
        self.serialBridge.write("G21\r\n") # mm
        self.wait_for_ok()
        self.serialBridge.write("G91\r\n") # rel
        self.wait_for_ok()
    
    def set_heating(self, percentage:int):
        print(f"Set heating to {percentage}%.")
        self.serialBridge.write(f"M104 S{percentage}\r\n")
        self.wait_for_ok()
        
    def update(self):
        self.serialBridge.flush()

        # update buffer size
        self.aprox_buffer = self.get_aprox_buffer()

        # execute commands until buffer is full
        t_0 = time.time()
        while self.aprox_buffer < MAX_BUFFER_SIZE:
            if time.time() - t_0 > Controller.SERIAL_TIMEOUT:
                raise RuntimeError("Timeout")
            # allowed to send TODO:
            # pointer = self.commandIterator.get_pointer()
            # command = self.commandIterator.get_text(pointer)
            # self.serialBridge.write(command + "\r\n")
            # self.wait_for_ok()
            self.aprox_buffer += 1
        
        # update metrics
        self.serialBridge.write("M105\r\n") # ask extruder temp
        self.wait_for_ok() # first ok
        self.wait_for_ok() # second ok
        t_0 = time.time()
        while True:
            if time.time() - t_0 > Controller.SERIAL_TIMEOUT:
                raise RuntimeError("Timeout")
            line = self.serialBridge.readline()
            if "ok T0:" in line:
                temp = int(line.split("ok T0:")[-1][:-2])
                break
        # check if temp is in bounds
        if abs(self.target_temperature - temp) > Controller.MAX_TEMP_OFFSET:
            self.logger.warn("Nozzle temperature is too far from the target.")
        self.register_event(events.UpdateNozzleTemperature(temp))

        # return all registered events
        cpy = self.registered_events
        self.register_event = []
        return cpy
    
    def register_event(self, event: events.Event):
        self.registered_events.append(event)

    def handle(self, event: events.Event):
        match event:
            case events.UpdateTargetTemperature(temperature=temp):
                self.target_temperature = temp
            case _:
               raise NotImplementedError("Event not catched.")
    
    def wait_for_ok(self):
        t_0 = time.time()
        while "ok\r\n" not in self.serialBridge.readline():
            if time.time() - t_0 > Controller.SERIAL_TIMEOUT:
                raise RuntimeError("Timeout")
        
    def get_aprox_buffer(self):
        self.serialBridge.write("G200\r\n") # custom command
        self.wait_for_ok()
        t_0 = time.time()
        while True:
            if time.time() - t_0 > Controller.SERIAL_TIMEOUT:
                raise RuntimeError("Timeout")
            line = self.serialBridge.readline()
            if "ok\r\n" == line:
                ...
            elif "$G200=" in line:
                # answer
                return int(line.split("=")[-1][:-2])

if __name__ == "__main__":
    c = Controller()
    while True:
        c.update()
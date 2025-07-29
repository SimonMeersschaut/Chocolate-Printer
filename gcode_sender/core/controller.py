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

    def __init__(self):
        self.commandIterator = SweepCommandIterator()
        self.serialBridge = SerialBridge()
        self.aprox_buffer = 0 # an estimate of the current planner buffer size in the arduino
        # this is a theoretical maximum

        self.gcode_file = ExampleGcodeFile()

        # handlers
        self._on_update_temp = None
        self.on_update_gcode_pointer = None
    
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
            # allowed to send
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
        yield events.UpdateNozzleTemperature(temp)
        return []

    def handle(self, event: events.Event):
        match event:
            case events.UpdateTargetTemperature(temperature=temp):
                print("Update target temp")
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
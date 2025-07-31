import time
from .serialBridge import SerialBridge
from .commandIterator import SweepCommandIterator
from .filehandler import GcodeHandler
import events


"""
TODO
"""
class Controller:
    MAX_BUFFER_SIZE = 1
    SERIAL_TIMEOUT = 5 # seconds
    MAX_TEMP_OFFSET = 5 # degrees celcius

    def __init__(self, logger):
        self.logger = logger
        self.registered_events = []

        self.gcode_file = GcodeHandler()
        self.register_event(events.NewGcodeFileHandler(self.gcode_file))
        self.serialBridge = SerialBridge()

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
    
    def set_heating(self, temperature:int):
        self.target_temperature = temperature
        self.serialBridge.write(f"M104 S{temperature}\r\n")
        self.wait_for_ok()
    
    def update(self):
        self.serialBridge.flush()

        # update buffer size
        cpy = self.gcode_file.aprox_buffer
        self.gcode_file.aprox_buffer = self.get_aprox_buffer()
        print(self.gcode_file.aprox_buffer)
        self.gcode_file.execution_line += max(0, cpy - self.gcode_file.aprox_buffer)
        self.register_event(events.SetGcodeLine(self.gcode_file.execution_line))

        # execute commands until buffer is full
        if self.gcode_file and self.gcode_file.playing:
            if self.gcode_file.com_line < self.gcode_file.get_size():
                t_0 = time.time()
                while self.gcode_file.aprox_buffer < Controller.MAX_BUFFER_SIZE:
                    if time.time() - t_0 > Controller.SERIAL_TIMEOUT:
                        raise RuntimeError("Timeout")
                    # allowed to send TODO:
                    if self.gcode_file.com_line >= self.gcode_file.get_size():
                        # Finished sending
                        break
                    else:
                        command = self.gcode_file.get_line(self.gcode_file.com_line)
                        if len(command) > 0 and command[0] != ';':
                            self.serialBridge.write(command + "\r\n")
                            self.wait_for_ok()

                            self.gcode_file.aprox_buffer += 1
                        self.gcode_file.com_line += 1
        
        # update metrics
        self.serialBridge.write("M105\r\n") # ask extruder temp
        self.wait_for_ok() # first ok
        self.wait_for_ok() # second ok
        t_0 = time.time()
        temp = -1
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

        self.serialBridge.flush()

        # return all registered events and flush
        cpy = self.registered_events
        self.registered_events = []
        return cpy
    
    def register_event(self, event: events.Event):
        self.registered_events.append(event)

    def handle(self, event: events.Event):
        match event:
            case events.UpdateTargetTemperature(temperature=temp):
                self.set_heating(temp)
            case events.PlayGcode:
                self.gcode_file.play()
            case events.PauseGcode:
                self.gcode_file.pause()
            case _:
               raise NotImplementedError("Event not catched: "+str(event))
    
    def wait_for_ok(self):
        t_0 = time.time()
        while "ok\r\n" not in self.serialBridge.readline():
            if time.time() - t_0 > Controller.SERIAL_TIMEOUT:
                raise RuntimeError("Timeout")
        
    def get_aprox_buffer(self):
        # self.serialBridge.flush()

        # self.serialBridge.write("G200\r\n") # custom command
        # t_0 = time.time()
        # while True:
        #     if time.time() - t_0 > Controller.SERIAL_TIMEOUT:
        #         raise RuntimeError("Timeout")
        #     line = self.serialBridge.readline()
        #     print(line)
        #     if "ok\r\n" == line:
        #         ...
        #     elif "$G200=" in line:
        #         # answer
        #         return int(line.split("=")[-1][:-2])
        return 0

if __name__ == "__main__":
    c = Controller()
    while True:
        c.update()
from serialBridge import SerialBridge
from commandIterator import CommandIterator, SweepCommandIterator

MAX_BUFFER_SIZE = 80

"""
TODO
"""
class Controller:
    def __init__(self):
        self.commandIterator = SweepCommandIterator()
        self.serialBridge = SerialBridge()
        self.aprox_buffer = 0 # an estimate of the current planner buffer size in the arduino
        # this is a theoretical maximum
    
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
            
    
    def update(self):
        ...
        # self.serialBridge.flush()

        # # execute command
        # if self.aprox_buffer < MAX_BUFFER_SIZE:
        #     # allowed to send
        #     pointer = self.commandIterator.get_pointer()
        #     command = self.commandIterator.get_text(pointer)
        #     self.serialBridge.write(command + "\r\n")
        #     self.wait_for_ok()
        #     self.aprox_buffer += 1
        # else:
        #     # not allowed; buffer is full
        #     # wait for buffer to shrink
        #     self.aprox_buffer = self.get_aprox_buffer()

    
    def wait_for_ok(self):
        while "ok\r\n" not in self.serialBridge.readline():
            ...
        
    def get_aprox_buffer(self):
        self.serialBridge.write("G200\r\n") # custom command
        
        while True:
            line = self.serialBridge.readline()
            if "ok\r\n" == line:
                ...
            elif "$G200=" in line:
                # answer
                return int(line.split("=")[:-2])


    
if __name__ == "__main__":
    c = Controller()
    while True:
        c.update()
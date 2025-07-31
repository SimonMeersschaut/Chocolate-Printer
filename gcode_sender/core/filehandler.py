from abc import ABC, abstractmethod


class GcodeHandler:
    def __init__(self):
        self.playing = False
        self.execution_line = 0 # the line that is estimated to be executing
        self.com_line = 0 # the last line that was sent to the COM
        self.aprox_buffer = 0 # an estimate of the current planner buffer size in the arduino
        # this is a theoretical maximum

        with open("../3d files/out.gcode", 'r') as f:
            self.gcode_lines = f.read().split('\n')

    def get_line(self, line: int):
        return self.gcode_lines[line]

    def get_size(self):
        return len(self.gcode_lines)
    
    def play(self):
        if not self.playing:
            self.playing = True
        
    def pause(self):
        if self.playing:
            self.playing = False
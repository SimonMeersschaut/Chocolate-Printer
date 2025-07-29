from abc import ABC, abstractmethod

class GcodeFile(ABC):
    @abstractmethod
    def __init__(self):
        ...

    def get_line(self, line:int):
        ...

class ExampleGcodeFile(GcodeFile):
    def __init__(self):
        self.gcode_lines = [
            "G21 ; Set units to millimeters",
            "G90 ; Use absolute positioning",
            "M82 ; Extruder in absolute mode",
            "M107 ; Turn off fan",
            "G28 X0 Y0 ; Home X and Y axes",
            "G28 Z0 ; Home Z axis",
            "G1 F5000 ; Lift nozzle",
            "M109 S200 ; Set extruder temperature and wait",
            "G1 X10 Y10 Z0.2 F1500 ; Move to start position and set first layer height",
            "G92 E0 ; Reset extruder position",
            "G1 E10 F600 ; Extrude 10mm of filament to prime nozzle",
            "G1 F1200 ; Set print speed",
            "G1 X20 Y20 E0.5 ; Print a small line",
            "M104 S0 ; Turn off hotend",
            "M140 S0 ; Turn off bed",
            "M84 ; Disable steppers"
        ]
    
    def get_line(self, line: int):
        return self.gcode_lines[line]
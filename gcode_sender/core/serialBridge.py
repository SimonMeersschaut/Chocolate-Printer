import serial

SERIAL_PORT = "COM5"

class SerialBridge:
    def __init__(self):
        ...
        
    def connect(self):
        self.ser = serial.Serial(
            SERIAL_PORT,
            baudrate=115200,
            timeout=1
        )
        self._buffer = ""
    
    def read(self):
        return self.ser.read()
        

    def write(self, data):
        print(f"> {data.strip()}")
        return self.ser.write(data.encode("utf-8"))

    def readline(self) -> str:
        char = True
        while char:
            char = self.read()
            if char:
                # print(char)
                char = char.decode("utf-8")
                self._buffer += char
                
                if char == '\n':
                    cpy = self._buffer
                    # print(cpy.strip())
                    self._buffer = "" # clear buffer
                    print(cpy)
                    return cpy
        return ""

    def flush(self):
        self.ser.flush()
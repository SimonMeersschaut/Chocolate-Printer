import serial
import time


with serial.Serial('COM4', 115200, timeout=1) as ser:
    print( ser.read() )
    # s = ser.read(10)        # read up to ten bytes (timeout)
    for i in range(4):
        print(ser.readline())

    # ser.write(b"$$\r\n")
    
    # input()
    ser.write(b"G21\r\n") # mm
    ser.write(b"G91\r\n") # rel
    # ser.write(b"G0 X-10\r\n")
    ser.write(b"G0 X+10\r\n")
    ser.write(b"G0 X-10\r\n")
    ser.write(b"G0 X+10\r\n")
    ser.write(b"G0 X-10\r\n")
    # ser.write(b"G0 X+10\r\n")
    # ser.write(b"G200\r\n") # echo

    while True:
        for i in range(5):
            line = ser.readline()   # read a '\n' terminated line
            print(line)
        ser.write(b"G200\r\n") # echo
        time.sleep(.5)
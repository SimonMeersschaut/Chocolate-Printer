from serial import Serial
import threading
import time

class Wire:
  def __init__(self) -> None:
    self.port = Serial('COM7', 115200)

    self.events = []
    self.out = []
    self.line = ''
  
  def wait_for(self, line) -> None:
    e = Event(line)
    self.events.append(e)
    while e.active:
      self.update()

  def send(self, line: str) -> None:
    self.port.write((line+'\n').encode('utf-8'))
  
  def update(self) -> None:
    self.readline()

    # if len(self.out) > 0:
    #   self.send(self.out.pop(0))
  
  def readline(self) -> None:
    while self.port.inWaiting():
      char = self.port.read().decode('utf-8')
      if char == '\n':
        print(self.line)
        self.broadcast_event(self.line)
        self.line = ''
      elif char == '\r':
        pass
      else:
        self.line += char
    
  def broadcast_event(self, line) -> None:
    for event in self.events:
      event.receive(line)

class Event:
  def __init__(self, line) -> None:
    self.line = line
    self.active = True

  def receive(self, line) -> None:
    if line == self.line:
      self.active = False
from wire import Wire

class Machine(Wire):
    def __init__(self) -> None:
        # setup COM
        super().__init__()
        self.wait_for("[MSG:'$H'|'$X' to unlock]")
        self.send('$X')
        self.wait_for('[MSG:Caution: Unlocked]')
        self.send('$$')
        self.wait_for('ok')
        # setup done
    
    def run_gcode(self, gcode: str) -> None:
        for line in gcode.split('\n'):
            self.execute(line)
        
        # self.wait_for('...')
    
    def execute(self, line):
        self.send(line)
        # self.wait_for('ok')
        # self.send('?')
        # input()


if __name__ == '__main__':
    machine = Machine()
    machine.run_gcode('F400 G1 X-16')
class Logger:
    def __init__(self, name: str):
        self.name = name
    
    def log(self, msg: str):
        print(f"[{self.name}] {msg}")
    
    def warn(self, msg: str):
        print(f"⚠️ [{self.name}] {msg}")
    
    def error(self, msg: str):
        print(f"🔴[{self.name}] {msg}")
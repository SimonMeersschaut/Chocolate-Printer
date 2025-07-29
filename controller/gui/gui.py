from abc import ABC, abstractmethod

class Gui(ABC):
    def __init__(self, on_update:callable):
        self.on_update = on_update

    @abstractmethod
    def run(self):
        """Runs the GUI application."""
        pass

    @abstractmethod
    def increment_pointer(self, current_pointer: int) -> int:
        """
        Increments the G-code pointer by one, cycling back to 0 if it reaches the end.
        Args:
            current_pointer: The current line number of the G-code.
        Returns:
            The new line number after incrementing.
        """
        pass

    @abstractmethod
    def update(self):
        self.on_update()
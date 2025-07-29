from abc import ABC, abstractmethod

# Define the abstract base class for the GUI interface
class AbstractPrinterGUI(ABC):
    @abstractmethod
    def add_temperature(self, temperature: int):
        """
        Abstract method: Called every second to add a temperature reading.
        Args:
            temperature: The temperature reading (integer).
        """
        pass

    @abstractmethod
    def set_pointer(self, pointer: int):
        """
        Abstract method: Sets the pointer in the gcode to a line position.
        Args:
            pointer: The 0-based index of the G-code line to highlight.
                     Set to -1 to clear highlighting.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Abstract method: Updates the GUI elements.
        """
        pass

    # You might also consider an abstract method for setting the slider callback
    # if it's a fundamental part of the interface, but for now, we'll keep it
    # as an optional constructor argument in the concrete class.
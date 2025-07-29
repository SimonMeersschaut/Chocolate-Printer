from core import Controller
from ui import Ui # Renamed Ui to PrinterGUI as per previous refactoring
import tkinter as tk # Tkinter root will be managed here

class PrinterApplication:
    """
    Orchestrates the 3D Printer Controller and its Graphical User Interface.
    Manages the setup, communication, and lifecycle of the application.
    """
    def __init__(self):
        self.controller = Controller()
        self.ui = Ui() # Pass the root to the UI

        self._update_job_id = None
        self.gcode_pointer = 0 # Manage gcode pointer state within the application

    def _connect_interfaces(self):
        """Establates the communication channels between the UI and Controller."""
        print("Interfaces connected successfully.")

    def _periodic_update(self):
        """
        Performs periodic updates for the controller and UI.
        This simulates continuous data flow and G-code progression.
        """
        if self.ui._running:
            for event in self.controller.update():
                self.ui.handle(event)

            for event in self.ui.update():
                self.controller.handle(event)
            
            # Schedule the next update
            self._update_job_id = self.ui.root.after(500, self._periodic_update)
        else:
            print("UI is not running, stopping periodic updates.")

    def run(self):
        """Initializes and runs the application."""
        print("Initializing application...")
        self.controller.connect() # Establish connection to hardware/simulator
        self.ui.initialize()     # Build the UI widgets

        self._connect_interfaces() # Wire up UI and Controller

        # Start the periodic update loop
        self._periodic_update()

        try:
            print("Starting Tkinter event loop...")
            self.ui.root.mainloop()
        except KeyboardInterrupt:
            print("\nCtrl+C detected. Exiting application.")
        finally:
            self.stop() # Ensure cleanup on exit

    def stop(self):
        """Performs cleanup when the application is closing."""
        print("Stopping application...")
        if self._update_job_id:
            self.ui.root.after_cancel(self._update_job_id)
        self.ui.close()
        self.controller.disconnect() # Assuming a disconnect method in Controller
        print("Application stopped.")
from .abstract_ui import AbstractUI
from .dark_theme import DarkTheme
from .heating_control import HeatingControl
from .temperature_chart import TemperatureChart
from .gcode_viewer import GcodeViewer
import events

import tkinter as tk
from tkinter import ttk

class TkinterUi(AbstractUI):
    def __init__(self, logger):
        self.logger = logger
        self.registered_events = []

        self.root = tk.Tk()
        self.root.title("3D Printer Control Panel")
        self.root.geometry("1000x800")
        self.root.configure(bg="#282c36")

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._running = True

    def initialize(self):
        """Creates and lays out all the GUI elements using specialized components."""
        
        # Apply dark theme using the global ttk.Style instance
        self.theme = DarkTheme(self.root) # Call without arguments now

        # Main Layout Frames
        top_frame = ttk.Frame(self.root, padding="10 10 10 10", style='DarkFrame.TFrame')
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        bottom_frame = ttk.Frame(self.root, padding="10 10 10 10", style='DarkFrame.TFrame')
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Temperature Chart Section
        temp_chart_frame = ttk.Frame(top_frame, padding="15", style='DarkFrame.TFrame')
        temp_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(temp_chart_frame, text="🔴 Current Temperature (Live Chart)", style='Heading.TLabel', foreground='#e74c3c').pack(anchor=tk.NW, pady=(0, 10))
        self.temperature_chart = TemperatureChart(temp_chart_frame)

        # Printer Settings Section
        settings_frame = ttk.Frame(top_frame, padding="15", style='DarkFrame.TFrame')
        settings_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(settings_frame, text="Printer Settings", style='Heading.TLabel').pack(anchor=tk.NW, pady=(0, 10))
        
        # Pass the slider_callback to HeatingControl
        def update_heating_temp(level):
            # update horizontal line in graph
            self.temperature_chart.set_target_temperature(level)
            # register event for controller
            self.register_event(events.UpdateTargetTemperature(level))
        self.heating_control = HeatingControl(settings_frame, on_update=update_heating_temp)


        # G-code Execution Section
        gcode_frame = ttk.Frame(bottom_frame, padding="15", style='DarkFrame.TFrame')
        gcode_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def handle(self, event: events.Event):
       match event:
            case events.UpdateNozzleTemperature(temperature=temp): # Match by type AND extract attribute
                self.temperature_chart.add_temperature(temp)
            case events.NewGcodeFileHandler(handler=handler):
               ... # TODO
            case _:
               raise NotImplementedError("Event not catched.")
        
    def register_event(self, event: events.Event):
        self.registered_events.append(event)

    def update(self):
        """
        Updates the GUI. This is typically handled by the Tkinter event loop,
        but can be called explicitly for immediate redraws if necessary.
        """
        self.root.update_idletasks()

        # return all registered events and clear
        cpy = self.registered_events
        self.registered_events = []
        return cpy

    def close(self):
        """Cleans up resources and closes the GUI."""
        self._running = False
        if self._update_job_id:
            self.root.after_cancel(self._update_job_id)
        self.temperature_chart.close() # Close Matplotlib figure
        self.root.destroy()

    def _on_closing(self):
        """Handles the window closing event."""
        print("Closing application...")
        self.close() # Reuse the close method for consistent cleanup
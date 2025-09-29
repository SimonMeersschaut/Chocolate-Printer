from .abstract_ui import AbstractUI
from .dark_theme import DarkTheme
from .monitor.temperature_chart import TemperatureChart
from .monitor.gcode import GcodeFrame
from .monitor.actions_control import ActionsControl
from .settings.heating_control import HeatingControl
from .settings.grbl_settings import GrblSettings
import events

import tkinter as tk
from tkinter import ttk

class TkinterUi(AbstractUI):
    MIN_WIDTH = 1000
    MIN_HEIGHT = 800

    def __init__(self, logger, update:callable):
        self.logger = logger
        self.registered_events = []

        self.root = tk.Tk()
        self.root.title("3D Printer Control Panel")
        self.root.geometry(f"{TkinterUi.MIN_WIDTH}x{TkinterUi.MIN_HEIGHT}")
        self.root.minsize(TkinterUi.MIN_WIDTH, TkinterUi.MIN_HEIGHT)
        self.root.configure(bg="#282c36")

        self.banner_label = tk.Label(self.root, text="Device Disconnected", fg="white", bg="red", font=("Arial", 14, "bold"), pady=5)

        self._update_job_id = None
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._running = True
        self._on_update = update

    def initialize(self):
        """Creates and lays out all the GUI elements using specialized components."""
        
        self.banner_label.pack(fill=tk.X, side=tk.TOP)
        
        # Apply dark theme using the global ttk.Style instance
        self.theme = DarkTheme(self.root)

        # Create a Notebook widget for tabs
        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create frames for each tab
        self.monitor_tab = ttk.Frame(self.notebook, style='DarkFrame.TFrame')
        self.settings_tab = ttk.Frame(self.notebook, style='DarkFrame.TFrame')

        self.notebook.add(self.monitor_tab, text='Monitor')
        self.notebook.add(self.settings_tab, text='Settings')

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        # --- Monitor Tab ---
        self._setup_monitor_tab()

        # --- Settings Tab ---
        self._setup_settings_tab()

    def _setup_monitor_tab(self):
        # Main Layout Frames for Monitor Tab
        top_frame = ttk.Frame(self.monitor_tab, padding="10 10 10 10", style='DarkFrame.TFrame')
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        bottom_frame = ttk.Frame(self.monitor_tab, padding="10 10 10 10", style='DarkFrame.TFrame')
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Temperature Chart Section
        temp_chart_frame = ttk.Frame(top_frame, padding="15", style='DarkFrame.TFrame')
        temp_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(temp_chart_frame, text="🔴 Current Temperature (Live Chart)", style='Heading.TLabel', foreground='#e74c3c').pack(anchor=tk.NW, pady=(0, 10))
        self.temperature_chart = TemperatureChart(temp_chart_frame)

        actions_frame = ttk.Frame(top_frame, padding="0 15 0 0", style='DarkFrame.TFrame')
        actions_frame.pack(fill=tk.X, pady=(10,0))
        self.actions_control = ActionsControl(
            actions_frame,
            play_callback=lambda: self.register_event(events.PlayGcode),
            home_callback=lambda: self.register_event(events.Home),
            pause_callback=lambda: self.register_event(events.PauseGcode),
            jog_callback=lambda movement: self.register_event(events.Jog(movement)),
            open_file_callback=lambda filename: self.register_event(events.NewGcodeFile(filename)),
        )

        # G-code Execution Section
        gcode_frame = ttk.Frame(bottom_frame, padding="15", style='DarkFrame.TFrame')
        self.gcode_viewer = GcodeFrame(gcode_frame)
        gcode_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _setup_settings_tab(self):
        settings_frame = ttk.Frame(self.settings_tab, padding="15", style='DarkFrame.TFrame')
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def update_heating_temp(tool, level):
            self.temperature_chart.set_target_temperature(tool, level)
            self.register_event(events.UpdateTargetTemperature(tool, level))
        self.heating_control = HeatingControl(settings_frame, on_update=update_heating_temp)

        separator = ttk.Separator(settings_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        self.grbl_settings = GrblSettings(
            settings_frame,
            send_callback=lambda setting, value: self.register_event(events.SendGrblSetting(setting, value))
        )
        self.grbl_settings.pack(fill=tk.BOTH, expand=True)


    def run(self):
        """TODO"""
        self._periodic_update()
        self.root.mainloop()
    
    def handle(self, event: events.Event):
        match event:
            case events.UpdateNozzleTemperature(tool=tool, temperature=temp):
                self.temperature_chart.add_temperatures({tool: temp})
            case events.NewGcodeFileHandler(handler=handler):
                self.gcode_viewer.set_fileHandler(handler)
            case events.SetGcodeLine(line=line):
                self.gcode_viewer.set_gcode_pointer(line)
            case events.ArduinoConnected():
                self.banner_label.pack_forget()
            case events.ArduinoDisconnected():
                self.banner_label.pack(fill=tk.X, side=tk.TOP, before=self.notebook)
                
            case events.GrblSettingsReceived(settings=settings):
                self.grbl_settings.set_settings(settings)

            case _:
                raise NotImplementedError("Event not caught: " + str(event))

        
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

    def _periodic_update(self):
        """
        Performs periodic updates for the controller and UI.
        This simulates continuous data flow and G-code progression.
        """
        if self._running:
            self._on_update()

            # Schedule the next update
            if self._running:
                self._update_job_id = self.root.after(500, self._periodic_update)
            else:
                print("UI is not running, stopping periodic updates.")
    
    def _on_closing(self):
        self._running = False
        self.temperature_chart.close() # Close Matplotlib figure
        self.root.destroy()
        if self._update_job_id:
            self.root.after_cancel(self._update_job_id)

    def _on_tab_changed(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 1:  # Settings tab
            self.register_event(events.RequestGrblSettings())
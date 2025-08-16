import tkinter as tk
from tkinter import ttk


class HeatingControl:
    """Manages the heating level slider and its interactions."""
    def __init__(self, parent_frame: ttk.Frame, on_update=None):
        self._on_update = on_update
        self.slider_value = 20
        ttk.Label(parent_frame, text="Extruder Temperature", style='DarkLabel.TLabel').pack(anchor=tk.NW, pady=(5, 0))
        self.heating_level_slider = tk.Scale(
            parent_frame,
            from_=20,
            # value=self.slider_value,
            to=50,
            orient=tk.HORIZONTAL,
            command=self._on_slider_change,
            tickinterval=5,
            showvalue=0
        )
        self.heating_level_slider.pack(fill=tk.X, pady=(5, 10))

        self.heating_level_label = ttk.Label(parent_frame, text=f"Heating Level: {self.slider_value}°C", style='DarkLabel.TLabel')
        self.heating_level_label.pack(anchor=tk.CENTER, pady=(10, 0))

    def _on_slider_change(self, value):
        """Callback for the heating level slider."""
        level = int(float(value))
        if self.slider_value != level:
            self.slider_value = level
            self.heating_level_label.config(text=f"Heating Level: {level}°C")
            if self._on_update: # Check if callback is set before calling
                self._on_update(level)

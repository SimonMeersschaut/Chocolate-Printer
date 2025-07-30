import tkinter as tk
from tkinter import ttk

class HeatingControl:
    """Manages the heating level slider and its interactions."""
    def __init__(self, parent_frame: ttk.Frame, on_update=None):
        self._on_update = on_update
        self.slider_value = 20
        ttk.Label(parent_frame, text="Heating", style='DarkLabel.TLabel').pack(anchor=tk.NW, pady=(5, 0))
        self.heating_level_slider = ttk.Scale(
            parent_frame,
            from_=20,
            value=self.slider_value,
            to=50,
            orient=tk.HORIZONTAL,
            command=self._on_slider_change,
            # IMPORTANT: Use a style name that matches the one defined for Horizontal Scales
            style="DarkScale.Horizontal.TScale" 
        )
        self.heating_level_slider.pack(fill=tk.X, pady=(5, 10))

        # Custom labels for slider ticks
        tick_frame = ttk.Frame(parent_frame, style='DarkFrame.TFrame')
        tick_frame.pack(fill=tk.X)
        for i in range(20, 46, 5):
            ttk.Label(tick_frame, text=str(i), style='DarkLabel.TLabel', font=('Inter', 8)).pack(side=tk.LEFT, expand=True)

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

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter import ttk
import tkinter as tk
from collections import deque

class TemperatureChart:
    """Manages the Matplotlib temperature chart and its associated data."""
    def __init__(self, parent_frame: ttk.Frame, max_chart_points: int = 60):
        self.temperature_data = deque(maxlen=max_chart_points)
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self._configure_chart_style()
        self.line, = self.ax.plot([], [], color='#2ecc71', linewidth=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.current_temp_label = ttk.Label(parent_frame, text="Current Temperature: --.--°C", style='DarkLabel.TLabel')
        self.current_temp_label.pack(anchor=tk.S, pady=(10, 0))
        
    def _configure_chart_style(self):
        """Sets up the visual style of the Matplotlib chart."""
        self.ax.set_facecolor('#1e2127')
        self.fig.patch.set_facecolor('#1e2127')
        self.ax.tick_params(axis='x', colors='#cccccc')
        self.ax.tick_params(axis='y', colors='#cccccc')
        self.ax.spines['bottom'].set_color('#cccccc')
        self.ax.spines['left'].set_color('#cccccc')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_xlabel("Time", color='#cccccc')
        self.ax.set_ylabel("Temperature (°C)", color='#cccccc')
        self.ax.set_title("", color='#ffffff')

    def add_temperature(self, temperature: int):
        """Adds a new temperature reading and updates the chart."""
        now = datetime.now()
        self.temperature_data.append((now, temperature))

        times = [d[0] for d in self.temperature_data]
        temps = [d[1] for d in self.temperature_data]

        if not times:
            return

        self.line.set_data(times, temps)
        self.ax.set_xlim(times[0], times[-1])
        
        if len(temps) > 1:
            self.ax.set_ylim(min(temps) - 2, max(temps) + 2)
        else:
            self.ax.set_ylim(temps[0] - 5, temps[0] + 5)

        num_ticks = min(5, len(times))
        if num_ticks > 0:
            tick_indices = [int(i * (len(times) - 1) / (num_ticks - 1)) for i in range(num_ticks)] if num_ticks > 1 else [0]
            self.ax.set_xticks([times[i] for i in tick_indices])
            self.ax.set_xticklabels([times[i].strftime("%H:%M:%S") for i in tick_indices], rotation=45, ha='right')
            self.ax.figure.autofmt_xdate()

        self.canvas.draw_idle()
        self.current_temp_label.config(text=f"Current Temperature: {temperature:.1f} °C")

    def close(self):
        """Closes the Matplotlib figure."""
        plt.close(self.fig)
    
    def set_target(self):
        ...
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
        self.line, = self.ax.plot([], [], color='#2ecc71', linewidth=2, label='Current Temp') # Add label for legend

        # --- New: Target Temperature Line ---
        self.target_temp_line = None # Initialize to None
        self._target_temperature = None # Store the target temperature

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.current_temp_label = ttk.Label(parent_frame, text="Current Temperature: --.--°C", style='DarkLabel.TLabel')
        self.current_temp_label.pack(anchor=tk.S, pady=(10, 0))

        # Add a legend to the chart
        self.ax.legend(loc='upper left', facecolor='#2c313a', edgecolor='#cccccc', labelcolor='white', framealpha=0.8)

        self.set_target_temperature(20)


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
        self.ax.set_title("Temperature Readings", color='#ffffff') # A more descriptive title


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
        
        # --- Update Y-axis limits to include target temp ---
        all_temps = list(temps)
        if self._target_temperature is not None:
            all_temps.append(self._target_temperature)

        if len(all_temps) > 1:
            min_y = min(all_temps) - 5 # Give a little padding
            max_y = max(all_temps) + 5
            self.ax.set_ylim(min_y, max_y)
        elif all_temps: # Only one point
            self.ax.set_ylim(all_temps[0] - 10, all_temps[0] + 10) # Default range if only one point
        else: # No data at all
            self.ax.set_ylim(0, 100) # Fallback if no data or target temp

        # Adjust x-tick labels dynamically
        num_ticks = min(5, len(times))
        if num_ticks > 0:
            tick_indices = [int(i * (len(times) - 1) / (num_ticks - 1)) for i in range(num_ticks)] if num_ticks > 1 else [0]
            self.ax.set_xticks([times[i] for i in tick_indices])
            self.ax.set_xticklabels([times[i].strftime("%H:%M:%S") for i in tick_indices], rotation=45, ha='right')
            self.ax.figure.autofmt_xdate()

        self.canvas.draw_idle()
        self.current_temp_label.config(text=f"Current Temperature: {temperature:.1f} °C")

    # --- New method to set target temperature ---
    def set_target_temperature(self, target_temp: float):
        """Sets the target temperature and updates the horizontal line on the chart."""
        self._target_temperature = target_temp

        if self.target_temp_line:
            self.target_temp_line.remove() # Remove existing line if any

        # Draw the new horizontal line
        # Use transform=self.ax.get_xaxis_transform() if you want it to stretch across the full x-axis
        # Alternatively, just specify xmin and xmax to stretch across the current view.
        self.target_temp_line = self.ax.axhline(
            y=target_temp,
            color='#FFD700', # Gold color for target
            linestyle='--',   # Dashed line
            linewidth=1.5,
            label=f'Target Temp: {target_temp}°C' # Label for legend
        )
        # Update the legend
        self.ax.legend(loc='upper left', facecolor='#2c313a', edgecolor='#cccccc', labelcolor='white', framealpha=0.8)

        # Ensure the y-axis limits adjust to include the new target temperature
        self.add_temperature(self.temperature_data[-1][1] if self.temperature_data else 0) # Trigger update
        self.canvas.draw_idle()


    def close(self):
        """Closes the Matplotlib figure."""
        plt.close(self.fig)
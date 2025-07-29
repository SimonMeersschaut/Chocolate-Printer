from abstract_printer_gui import AbstractPrinterGUI
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class PrinterGUI(AbstractPrinterGUI):
    def __init__(self, master_root, slider_callback=None):
        """
        Initializes the 3D Printer Control Panel GUI.

        Args:
            master_root: The Tkinter root window.
            slider_callback: An optional callback function for the heating level slider.
                             It will receive the slider's current value (0-100) as an argument.
        """
        self.root = master_root
        self.root.title("3D Printer Control Panel")
        self.root.geometry("1000x800") # Set a default size for better layout
        self.root.configure(bg="#282c36") # Dark background

        self.slider_value = 50
        self.slider_callback = slider_callback

        # --- Data storage for the chart ---
        self.temperature_data = [] # Stores (timestamp, temperature) tuples
        self.time_labels = []      # Stores formatted time strings for x-axis
        self.max_chart_points = 20 # Max points to display on the chart

        self.current_gcode_pointer = -1 # -1 means no line is selected

        self._create_widgets()

    def _create_widgets(self):
        """Creates and lays out all the GUI elements."""

        # --- Main Layout Frames ---
        # Top row: Temperature Chart and Printer Settings
        top_frame = ttk.Frame(self.root, padding="10 10 10 10", style='DarkFrame.TFrame')
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bottom row: G-code Execution
        bottom_frame = ttk.Frame(self.root, padding="10 10 10 10", style='DarkFrame.TFrame')
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Styles for ttk widgets ---
        style = ttk.Style()
        style.theme_use('clam') # Use 'clam' theme for better dark mode compatibility
        style.configure('DarkFrame.TFrame', background='#2c313a', relief='flat')
        style.configure('DarkLabel.TLabel', background='#2c313a', foreground='#ffffff', font=('Inter', 12))
        style.configure('Heading.TLabel', background='#2c313a', foreground='#ffffff', font=('Inter', 16, 'bold'))
        style.configure('DarkText.TText', background='#1e2127', foreground='#ffffff', insertbackground='#ffffff', font=('monospace', 10))
        style.configure('DarkButton.TButton', background='#4a90e2', foreground='#ffffff', font=('Inter', 12, 'bold'), borderwidth=0, focusthickness=3, focuscolor='none')
        style.map('DarkButton.TButton',
                  background=[('active', '#357abd')],
                  foreground=[('active', '#ffffff')])
        
        # Define the layout for the custom scale style
        style.layout('DarkScale.Horizontal',
                     [('Horizontal.Scale.trough',
                       {'children': [('Horizontal.Scale.slider',
                                      {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'})])
        style.configure('DarkScale.Horizontal', background='#2c313a', troughcolor='#1e2127', slidercolor='#4a90e2',
                        foreground='#ffffff', highlightbackground='#2c313a', borderwidth=0)


        # --- Temperature Chart Section ---
        temp_chart_frame = ttk.Frame(top_frame, padding="15", style='DarkFrame.TFrame')
        temp_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(temp_chart_frame, text="🔴 Current Temperature (Live Chart)", style='Heading.TLabel', foreground='#e74c3c').pack(anchor=tk.NW, pady=(0, 10))

        # Matplotlib figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.ax.set_facecolor('#1e2127') # Chart background
        self.fig.patch.set_facecolor('#1e2127') # Figure background
        self.ax.tick_params(axis='x', colors='#cccccc') # X-axis tick labels color
        self.ax.tick_params(axis='y', colors='#cccccc') # Y-axis tick labels color
        self.ax.spines['bottom'].set_color('#cccccc') # X-axis line color
        self.ax.spines['left'].set_color('#cccccc') # Y-axis line color
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_xlabel("Time", color='#cccccc')
        self.ax.set_ylabel("Temperature (°C)", color='#cccccc')
        self.ax.set_title("", color='#ffffff') # Title will be updated dynamically

        self.line, = self.ax.plot([], [], color='#2ecc71', linewidth=2) # Initialize empty plot line

        self.canvas = FigureCanvasTkAgg(self.fig, master=temp_chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.current_temp_label = ttk.Label(temp_chart_frame, text="Current Temperature: --.--°C", style='DarkLabel.TLabel')
        self.current_temp_label.pack(anchor=tk.S, pady=(10, 0))


        # --- Printer Settings Section ---
        settings_frame = ttk.Frame(top_frame, padding="15", style='DarkFrame.TFrame')
        settings_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(settings_frame, text="Printer Settings", style='Heading.TLabel').pack(anchor=tk.NW, pady=(0, 10))

        ttk.Label(settings_frame, text="Heating", style='DarkLabel.TLabel').pack(anchor=tk.NW, pady=(5, 0))

        self.heating_level_slider = ttk.Scale(
            settings_frame,
            from_=0,
            value=self.slider_value,
            to=100,
            orient=tk.HORIZONTAL,
            command=self._on_slider_change,
            style='DarkScale.Horizontal'
        )
        
        self.heating_level_slider.pack(fill=tk.X, pady=(5, 10))
        
        # Custom labels for slider ticks (0, 10, 20, ..., 100)
        tick_frame = ttk.Frame(settings_frame, style='DarkFrame.TFrame')
        tick_frame.pack(fill=tk.X)
        for i in range(0, 101, 10):
            ttk.Label(tick_frame, text=str(i), style='DarkLabel.TLabel', font=('Inter', 8)).pack(side=tk.LEFT, expand=True)

        self.heating_level_label = ttk.Label(settings_frame, text=f"Heating Level: {self.slider_value}%", style='DarkLabel.TLabel')
        self.heating_level_label.pack(anchor=tk.CENTER, pady=(10, 0))


        # --- G-code Execution Section ---
        gcode_frame = ttk.Frame(bottom_frame, padding="15", style='DarkFrame.TFrame')
        gcode_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(gcode_frame, text="G-code Execution", style='Heading.TLabel').pack(anchor=tk.NW, pady=(0, 10))

        # G-code text area
        self.gcode_text = tk.Text(gcode_frame, wrap=tk.WORD, height=15, width=80,
                                  background='#1e2127', foreground='#ffffff',
                                  insertbackground='#ffffff', font=('monospace', 10),
                                  borderwidth=0, highlightthickness=0, relief='flat')
        self.gcode_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # TODO # Populate G-code text area
        # for line in self.gcode_lines:
        #     self.gcode_text.insert(tk.END, line + "\n")
        # self.gcode_text.config(state=tk.DISABLED) # Make it read-only

        # Define a tag for highlighting the current line
        self.gcode_text.tag_configure("current_line", background="#3a4049", foreground="#2ecc71", font=('monospace', 10, 'bold'))
        self.gcode_text.tag_configure("comment", foreground="#888888") # For comments in G-code

        # Apply comment tags initially
        # for i, line in enumerate(self.gcode_lines):
        #     if ';' in line:
        #         comment_start = line.find(';')
        #         self.gcode_text.tag_add("comment", f"{i+1}.{comment_start}", f"{i+1}.end")

        # Initial pointer setup
        self.set_pointer(0) # Set pointer to the first line

    def _on_slider_change(self, value):
        """Callback for the heating level slider."""
        level = int(float(value))
        if self.slider_value != level:
            self.slider_value = level
            # change detected
            self.heating_level_label.config(text=f"Heating Level: {level}%")
            if self.slider_callback:
                self.slider_callback(level)

    def add_temperature(self, temperature: int):
        """
        Called every second to add a temperature reading to the live chart.

        Args:
            temperature: The temperature reading (integer).
        """
        now = datetime.now()
        self.temperature_data.append((now, temperature))
        self.time_labels.append(now.strftime("%H:%M:%S"))

        # Keep only the last 'max_chart_points' data points
        if len(self.temperature_data) > self.max_chart_points:
            self.temperature_data = self.temperature_data[-self.max_chart_points:]
            self.time_labels = self.time_labels[-self.max_chart_points:]

        times = [d[0] for d in self.temperature_data]
        temps = [d[1] for d in self.temperature_data]

        self.line.set_data(times, temps)
        self.ax.set_xlim(times[0], times[-1])
        self.ax.set_ylim(min(temps) - 2, max(temps) + 2) # Dynamic Y-axis limits
        self.ax.set_xticks(times[::max(1, len(times) // 5)]) # Show fewer ticks if many points
        self.ax.set_xticklabels([t.strftime("%H:%M:%S") for t in times[::max(1, len(times) // 5)]], rotation=45, ha='right')
        self.ax.figure.autofmt_xdate() # Auto-format date labels

        self.canvas.draw_idle() # Redraw the chart efficiently

        self.current_temp_label.config(text=f"Current Temperature: {temperature:.1f}°C")

    def set_pointer(self, pointer: int):
        """
        Sets the pointer in the gcode to a specific line position.

        Args:
            pointer: The 0-based index of the G-code line to highlight.
                     Set to -1 to clear highlighting.
        """
        # Remove previous highlighting
        self.gcode_text.tag_remove("current_line", "1.0", tk.END)

        # if 0 <= pointer < len(self.gcode_lines):
        #     self.current_gcode_pointer = pointer
        #     # Add highlighting to the new line
        #     start_index = f"{pointer + 1}.0"
        #     end_index = f"{pointer + 1}.end"
        #     self.gcode_text.tag_add("current_line", start_index, end_index)
        #     # Scroll to the highlighted line
        #     self.gcode_text.see(start_index)
        # else:
        #     self.current_gcode_pointer = -1 # No line highlighted

    def update(self):
        """
        Updates the GUI. This is typically handled by the Tkinter event loop,
        but can be called explicitly for immediate redraws if necessary.
        """
        self.root.update_idletasks()
        # The main loop handles most updates, but this can be useful for
        # forcing updates in specific scenarios outside the event loop.


from .gui import Gui # Changed from .gui to gui for direct execution in a flat structure
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta
from collections import deque

# Sample G-code for demonstration (kept global as it represents the file content)
sample_gcode = """
G21 ; Set units to millimeters
G90 ; Use absolute positioning
M82 ; Extruder in absolute mode
M107 ; Turn off fan
G28 X0 Y0 ; Home X and Y axes
G28 Z0 ; Home Z axis
G1 Z5 F5000 ; Lift nozzle
M109 S200 ; Set extruder temperature and wait
G92 E0 ; Reset extruder position
G1 F200 E10 ; Extrude 10mm of filament
G92 E0 ; Reset extruder position again
G1 X10 Y10 Z0.2 F1500 ; Move to start position for print
G1 X100 Y10 Z0.2 E15 F1500 ; Print first line
G1 X100 Y20 Z0.2 E20 F1500 ; Print second line
G1 X10 Y20 Z0.2 E25 F1500 ; Print third line
G1 X10 Y30 Z0.2 E30 F1500 ; Print fourth line
G1 X100 Y30 Z0.2 E35 F1500 ; Print fifth line
G1 X100 Y40 Z0.2 E40 F1500 ; Print sixth line
G1 X10 Y40 Z0.2 E45 F1500 ; Print seventh line
G1 X10 Y50 Z0.2 E50 F1500 ; Print eighth line
G1 X100 Y50 Z0.2 E55 F1500 ; Print ninth line
G1 X100 Y60 Z0.2 E60 F1500 ; Print tenth line
M104 S0 ; Turn off extruder heater
M140 S0 ; Turn off bed heater
G91 ; Use relative positioning
G1 Z10 F3000 ; Lift nozzle to clear print
G90 ; Use absolute positioning
G28 X0 Y0 ; Home X and Y axes
M84 ; Disable steppers
"""
gcode_lines = [line.strip() for line in sample_gcode.strip().split('\n') if line.strip()]

class Dashgui(Gui):
    MAX_TEMP_DATA_POINTS = 40
    GCODE_DISPLAY_FRAME_SIZE = 10 # Number of G-code lines to display

    def __init__(self):
        # Initialize the base Gui class with a dummy on_update function.
        # In a Dash app, the main update logic is handled by Dash callbacks.
        super().__init__(on_update=lambda: None)
        # Initialize the Dash app
        self.app = dash.Dash(__name__,
                            external_stylesheets=['https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'])

        # Instance deques to store temperature data for the live chart
        self.temperature_data = deque(maxlen=Dashgui.MAX_TEMP_DATA_POINTS)
        self.time_data = deque(maxlen=Dashgui.MAX_TEMP_DATA_POINTS)

        # Initialize with some dummy data for the first view
        for i in range(Dashgui.MAX_TEMP_DATA_POINTS):
            self.time_data.append(datetime.now() - timedelta(seconds=Dashgui.MAX_TEMP_DATA_POINTS - 1 - i))
            self.temperature_data.append(random.uniform(28, 32)) # Initial random temperatures within the new range

        # Define the layout of the application
        self.app.layout = html.Div(
            className="min-h-screen bg-gray-900 text-white p-8 font-sans flex flex-col items-center",
            children=[
                html.H1(
                    "3D Printer Control Panel",
                    className="text-4xl font-bold text-center mb-10 text-blue-400"
                ),

                # Top section: Temperature Chart and Settings
                html.Div(
                    className="flex flex-col md:flex-row gap-8 w-full max-w-4xl mb-8",
                    children=[
                        # Temperature Display Card (now with a live line chart)
                        html.Div(
                            className="bg-gray-800 rounded-lg shadow-lg p-6 flex-1",
                            children=[
                                html.H2("🔴 Current Temperature (Live Chart)", className="text-2xl font-semibold mb-4 text-gray-200"),
                                dcc.Graph(
                                    id='temperature-graph',
                                    config={'displayModeBar': False},
                                    style={'height': '300px'},
                                    figure={
                                        'data': [
                                            go.Scatter(
                                                x=list(self.time_data),
                                                y=list(self.temperature_data),
                                                mode='lines+markers',
                                                name='Nozzle Temperature',
                                                line=dict(color='#4A90E2', width=3),
                                                marker=dict(color='#22C55E', size=8)
                                            )
                                        ],
                                        'layout': go.Layout(
                                            paper_bgcolor="rgba(0,0,0,0)",
                                            plot_bgcolor="rgba(0,0,0,0)",
                                            font={'color': "#E2E8F0", 'family': "Inter, sans-serif"},
                                            margin=dict(l=50, r=20, t=40, b=50),
                                            xaxis=dict(
                                                title='Time',
                                                showgrid=True,
                                                gridcolor='#4A5568',
                                                zeroline=False,
                                                tickfont=dict(color='#A0AEC0')
                                            ),
                                            yaxis=dict(
                                                title='Temperature (°C)',
                                                range=[25, 40], # Fixed range for temperature
                                                showgrid=True,
                                                gridcolor='#4A5568',
                                                zeroline=False,
                                                tickfont=dict(color='#A0AEC0')
                                            ),
                                            hovermode='x unified'
                                        )
                                    }
                                ),
                                html.Div(id='temperature-output', className="text-xl text-center mt-4 text-gray-300"),
                                # Interval component to update the graph and G-code every second
                                dcc.Interval(
                                    id='interval-component',
                                    interval=0.5 * 1000, # in milliseconds (0.5 seconds)
                                    n_intervals=0
                                )
                            ]
                        ),

                        # Settings Control Card
                        html.Div(
                            className="bg-gray-800 rounded-lg shadow-lg p-6 flex-1",
                            children=[
                                html.H2("Printer Settings", className="text-2xl font-semibold mb-4 text-gray-200"),
                                html.Label("Heating", className="block text-lg mb-2 text-gray-300"),
                                dcc.Slider(
                                    id='temperature-slider',
                                    min=0,
                                    max=100,
                                    step=5,
                                    value=50, # Initial slider value
                                    marks={i: {'label': str(i), 'style': {'color': '#9CA3AF'}} for i in range(0, 101, 10)},
                                    className="mb-6",
                                    tooltip={"placement": "bottom", "always_visible": True}
                                ),
                                html.Div(id='slider-output', className="text-xl text-center mt-4 text-gray-300")
                            ]
                        )
                    ]
                ),

                # G-code Viewer Section
                html.Div(
                    className="bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-4xl",
                    children=[
                        html.H2("G-code Execution", className="text-2xl font-semibold mb-4 text-gray-200"),
                        html.Div(
                            id='gcode-display',
                            className="bg-gray-900 p-4 rounded-md font-mono text-sm overflow-auto mb-4",
                            style={'height': '250px', 'lineHeight': '1.5'}
                        ),
                        # Hidden dcc.Store to keep track of the current G-code line pointer
                        dcc.Store(id='current-line-pointer', data=0)
                    ]
                )
            ]
        )

        # Register callbacks
        self._register_callbacks()

    def increment_pointer(self, current_pointer: int) -> int:
        """
        Increments the G-code pointer by one, cycling back to 0 if it reaches the end.
        Args:
            current_pointer: The current line number of the G-code.
        Returns:
            The new line number after incrementing.
        """
        return (current_pointer + 1) % len(gcode_lines)

    def update(self):
        """
        Implements the abstract update method from Gui.
        In this Dash context, it primarily serves to satisfy the ABC requirement.
        The actual UI updates are handled by Dash callbacks.
        """
        self.on_update() # Calls the dummy lambda passed in __init__

    def _register_callbacks(self):
        # Callback to update the temperature graph and display based on slider and interval
        @self.app.callback(
            [Output('temperature-graph', 'figure'),
            Output('temperature-output', 'children'),
            Output('slider-output', 'children')],
            [Input('temperature-slider', 'value'),
            Input('interval-component', 'n_intervals')]
        )
        def update_temperature_and_slider_output(heating_percentage, n_intervals):
            # Call the abstract update method from the base Gui class.
            # This will execute the dummy lambda passed in __init__.
            self.update()

            # Map heating_percentage (0-100) to temperature range (25-40)
            base_temp = 25 + (heating_percentage / 100) * (40 - 25)

            fluctuation = random.uniform(-1, 1) # Smaller fluctuation for tighter range
            current_temp = max(25, min(40, base_temp + fluctuation)) # Keep within bounds of 25-40

            # Append new data to the deques
            self.time_data.append(datetime.now())
            self.temperature_data.append(current_temp)

            # Update the line chart figure
            updated_figure = go.Figure(
                data=[
                    go.Scatter(
                        x=list(self.time_data),
                        y=list(self.temperature_data),
                        mode='lines+markers',
                        name='Nozzle Temperature',
                        line=dict(color='#4A90E2', width=3),
                        marker=dict(color='#22C55E', size=8)
                    )
                ],
                layout=go.Layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': "#E2E8F0", 'family': "Inter, sans-serif"},
                    margin=dict(l=50, r=20, t=40, b=50),
                    xaxis=dict(
                        title='Time',
                        showgrid=True,
                        gridcolor='#4A5568',
                        zeroline=False,
                        tickfont=dict(color='#A0AEC0')
                    ),
                    yaxis=dict(
                        title='Temperature (°C)',
                        range=[25, 40],
                        showgrid=True,
                        gridcolor='#4A5568',
                        zeroline=False,
                        tickfont=dict(color='#A0AEC0')
                    ),
                    hovermode='x unified'
                )
            )

            temp_text = f"Current Temperature: {current_temp:.1f}°C"
            slider_text = f"Heating Level: {heating_percentage}%"
            return updated_figure, temp_text, slider_text

        # Callback to update the G-code display automatically
        @self.app.callback(
            [Output('gcode-display', 'children'),
            Output('current-line-pointer', 'data')],
            [Input('interval-component', 'n_intervals')], # Triggered by the interval
            [State('current-line-pointer', 'data')]
        )
        def update_gcode_display(n_intervals, current_line_pointer):
            # Call the increment_pointer method of the Dashgui instance
            new_pointer = self.increment_pointer(current_line_pointer)

            # Calculate the range of lines to display
            # Ensure 5 lines before and 4 lines after (total 10 with current)
            start_index = max(0, new_pointer - 5)
            end_index = min(len(gcode_lines), new_pointer + 5)

            # Adjust start/end if near beginning or end of file to maintain FRAME_SIZE
            if end_index - start_index < self.GCODE_DISPLAY_FRAME_SIZE:
                if new_pointer < 5: # Near beginning
                    start_index = 0
                    end_index = min(len(gcode_lines), self.GCODE_DISPLAY_FRAME_SIZE)
                elif new_pointer >= len(gcode_lines) - 5: # Near end
                    end_index = len(gcode_lines)
                    start_index = max(0, len(gcode_lines) - self.GCODE_DISPLAY_FRAME_SIZE)

            display_lines = []
            for i in range(start_index, end_index):
                line_text = gcode_lines[i]
                if i == new_pointer:
                    # Highlight the current line
                    display_lines.append(
                        html.Div(
                            [
                                html.Span("-> ", className="text-green-400 font-bold"),
                                html.Code(line_text, className="text-green-300 bg-gray-700 px-2 py-1 rounded")
                            ],
                            className="mb-1"
                        )
                    )
                else:
                    display_lines.append(
                        html.Div(
                            html.Code(line_text, className="text-gray-400"),
                            className="mb-1"
                        )
                    )
            return display_lines, new_pointer

    def run(self):
        """Runs the Dash GUI application."""
        self.app.run(debug=True)

# Main execution block
if __name__ == '__main__':
    gui = Dashgui()
    gui.run()

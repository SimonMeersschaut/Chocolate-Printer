import tkinter as tk
from tkinter import ttk

class ActionsControl:
    """Manages the Play, Pause, Stop, and Jog buttons."""
    def __init__(self, parent_frame: ttk.Frame, play_callback=None, pause_callback=None, stop_callback=None,
                 jog_callback=None):
        self.play_callback = play_callback
        self.pause_callback = pause_callback
        self.stop_callback = stop_callback
        self.jog_callback = jog_callback  # Accept a general jog callback

        ttk.Label(parent_frame, text="Actions", style='Heading.TLabel').pack(anchor=tk.NW, pady=(0, 10))

        button_frame = ttk.Frame(parent_frame, style='DarkFrame.TFrame')
        button_frame.pack(fill=tk.X, pady=(5, 0))

        self.play_button = ttk.Button(
            button_frame,
            text="▶ Play",
            command=self._on_play,
            style='DarkButton.TButton'
        )
        self.play_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

        self.pause_button = ttk.Button(
            button_frame,
            text="⏸ Pause",
            command=self._on_pause,
            style='DarkButton.TButton'
        )
        self.pause_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

        # Jog buttons section
        jog_frame = ttk.Frame(parent_frame, style='DarkFrame.TFrame')
        jog_frame.pack(pady=(10, 0))

        directions = [
            ("X-", [-1, 0, 0], 0, 0), ("X+", [1, 0, 0], 0, 1),
            ("Y-", [0, -1, 0], 1, 0), ("Y+", [0, 1, 0], 1, 1),
            ("Z-", [0, 0, -1], 2, 0), ("Z+", [0, 0, 1], 2, 1),
        ]

        for label, movement, row, col in directions:
            btn = ttk.Button(
                jog_frame,
                text=label,
                command=lambda movement=movement: self._on_jog(movement),
                style='DarkButton.TButton'
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Optional: make buttons stretch to fill the frame
        for i in range(3):
            jog_frame.rowconfigure(i, weight=1)
        for i in range(2):
            jog_frame.columnconfigure(i, weight=1)

    def _on_play(self):
        if self.play_callback:
            self.play_callback()

    def _on_pause(self):
        if self.pause_callback:
            self.pause_callback()

    def _on_jog(self, axis):
        if self.jog_callback:
            self.jog_callback(axis)

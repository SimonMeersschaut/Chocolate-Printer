import tkinter as tk
from tkinter import ttk

class ActionsControl:
    """Manages the Play, Pause, and Stop buttons."""
    def __init__(self, parent_frame: ttk.Frame, play_callback=None, pause_callback=None, stop_callback=None):
        self.play_callback = play_callback
        self.pause_callback = pause_callback
        self.stop_callback = stop_callback

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

    def _on_play(self):
        if self.play_callback:
            self.play_callback()

    def _on_pause(self):
        if self.pause_callback:
            self.pause_callback()

    # def set_callbacks(self, play_cb, pause_cb):
        # """Allows setting/updating callbacks after initialization."""
        # self.play_callback = play_cb
        # self.pause_callback = pause_cb
import tkinter as tk
from tkinter import ttk

class GcodeViewer:
    """Manages the G-code text area, highlighting, and scrolling."""
    def __init__(self, parent_frame: ttk.Frame, gcode_file_controller):
        self.gcode_file = gcode_file_controller # This assumes gcode_file_controller has get_size() and get_line()
        self.current_gcode_pointer = -1

        ttk.Label(parent_frame, text="G-code Execution", style='Heading.TLabel').pack(anchor=tk.NW, pady=(0, 10))

        self.gcode_text = tk.Text(parent_frame, wrap=tk.WORD, height=15, width=80,
                                  background='#1e2127', foreground='#ffffff',
                                  insertbackground='#ffffff', font=('monospace', 10),
                                  borderwidth=0, highlightthickness=0, relief='flat')
        self.gcode_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self._populate_gcode_text()
        self.gcode_text.config(state=tk.DISABLED)

        self.gcode_text.tag_configure("current_line", background="#3a4049", foreground="#2ecc71", font=('monospace', 10, 'bold'))
        self.gcode_text.tag_configure("comment", foreground="#888888")
        self._apply_comment_tags()

        self.set_gcode_pointer(0)

    def _populate_gcode_text(self):
        """Populates the G-code text area with lines from the G-code file."""
        for i in range(self.gcode_file.get_size()):
            self.gcode_text.insert(tk.END, self.gcode_file.get_line(i) + "\n")

    def _apply_comment_tags(self):
        """Applies comment highlighting to G-code lines."""
        for i in range(self.gcode_file.get_size()):
            line = self.gcode_file.get_line(i)
            if ';' in line:
                comment_start = line.find(';')
                self.gcode_text.tag_add("comment", f"{i+1}.{comment_start}", f"{i+1}.end")

    def set_gcode_pointer(self, pointer: int):
        """
        Sets the pointer in the gcode to a specific line position.
        Auto-scrolls to the highlighted line.
        """
        self.gcode_text.tag_remove("current_line", "1.0", tk.END)

        if 0 <= pointer < self.gcode_file.get_size():
            self.current_gcode_pointer = pointer
            start_index = f"{pointer + 1}.0"
            end_index = f"{pointer + 1}.end"
            self.gcode_text.tag_add("current_line", start_index, end_index)
            self.gcode_text.see(start_index)
        else:
            self.current_gcode_pointer = -1
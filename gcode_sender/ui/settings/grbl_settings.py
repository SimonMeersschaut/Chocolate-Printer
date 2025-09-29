import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class GrblSettings(ttk.Frame):
    def __init__(self, parent, send_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.send_callback = send_callback
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=10)

        self.load_button = ttk.Button(button_frame, text="Load from File", command=self.load_settings)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(button_frame, text="Save to File", command=self.save_settings)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.send_button = ttk.Button(button_frame, text="Send to Printer", command=self.send_settings)
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Treeview for settings
        self.tree = ttk.Treeview(self, columns=("setting", "value", "description"), show="headings")
        self.tree.heading("setting", text="Setting")
        self.tree.heading("value", text="Value")
        self.tree.heading("description", text="Description")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_settings(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return

        with open(filepath, "r") as f:
            lines = f.readlines()

        # Clear existing items
        for i in self.tree.get_children():
            self.tree.delete(i)

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split("=")
            if len(parts) == 2:
                setting = parts[0]
                value = parts[1]
                self.tree.insert("", "end", values=(setting, value, ""))

    def save_settings(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return

        with open(filepath, "w") as f:
            for child in self.tree.get_children():
                item = self.tree.item(child)
                f.write(f"{item['values'][0]}={item['values'][1]}\n")

    def send_settings(self):
        if not self.send_callback:
            return

        for child in self.tree.get_children():
            item = self.tree.item(child)
            setting = item['values'][0]
            value = item['values'][1]
            self.send_callback(setting, value)

    def set_settings(self, settings):
        # Clear existing items
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Insert new settings
        for setting in settings:
            self.tree.insert("", "end", values=(setting["setting"], setting["value"], setting["description"]))

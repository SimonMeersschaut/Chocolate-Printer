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

        self.save_and_send_button = ttk.Button(button_frame, text="Save and Send", command=self.send_settings)
        self.save_and_send_button.pack(side=tk.LEFT, padx=5)

        # Treeview for settings
        self.tree = ttk.Treeview(self, columns=("setting", "value", "description"), show="headings")
        self.tree.heading("setting", text="Setting")
        self.tree.heading("value", text="Value")
        self.tree.heading("description", text="Description")
        self.tree.pack(fill=tk.BOTH, expand=True)



    def send_settings(self):
        # Save to file
        with open("firmware.settings", "w") as f:
            for child in self.tree.get_children():
                item = self.tree.item(child)
                f.write(f"{item['values'][0]}={item['values'][1]}\n")

        # Send to printer
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

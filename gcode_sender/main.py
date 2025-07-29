from controller import Controller
from printer_gui import PrinterGUI
import tkinter as tk
import random


if __name__ == "__main__":
    controller = Controller()

    root = tk.Tk()
    gui = PrinterGUI(root, slider_callback=controller.set_heating)

    def update():
        controller.update()
        gui.add_temperature(random.randint(30, 40))
        
        root.after(1000, update) # Call again after 1000ms (1 second)

    # Start the temperature simulation
    update()

    # Run the Tkinter event loop
    root.mainloop()

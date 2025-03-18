import tkinter as tk
from tkinter import ttk
import queue

# Defining a global queue to receive updates from main
data_queue = queue.Queue()

def update_table():
    """Check for new data in the queue and update the table."""
    while not data_queue.empty():
        time_step, x, y, theta = data_queue.get()
        tree.insert("", "end", values=(time_step, round(x, 3), round(y, 3), round(theta, 3))) # Rounding estimate to 3 decimal places

    root.after(100, update_table)  # Schedule the function to run again

# Running the GUI
def run_gui():
    """Initialize and run the Tkinter GUI."""
    global root, tree  # Make them access to update_table()
    root = tk.Tk()
    root.title("Live Robot Position Table")

    # Creating table
    tree = ttk.Treeview(root, columns=("Time", "X", "Y", "Theta"), show="headings")
    tree.heading("Time", text="Time")
    tree.heading("X", text="X Position")
    tree.heading("Y", text="Y Position")
    tree.heading("Theta", text="Theta")

    tree.pack(expand=True, fill="both")

    update_table()  # Checking for updates

    root.mainloop()

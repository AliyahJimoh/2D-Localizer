import queue
import tkinter as tk
from tkinter import ttk


def update_table():
    """Check for new data in the queue and update the table."""
    global data_queue
    while not data_queue.empty():
        try:
            time_step, x, y, theta = data_queue.get_nowait()
            tree.insert(
                "", "end", values=(time_step, round(x, 3), round(y, 3), round(theta, 3))
            )  # Round all to 3 decimal places
        except queue.Empty:
            pass

    root.after(100, update_table)  # Re-run after 100ms


def run_gui(queue):
    """Start the Tkinter GUI and link it to the queue."""
    global root, tree, data_queue
    data_queue = queue
    root = tk.Tk()
    root.title("Estimated Pose Table")

    tree = ttk.Treeview(root, columns=("Position", "X", "Y", "Theta"), show="headings")
    for col in ("Position", "X", "Y", "Theta"):
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.pack(expand=True, fill="both")

    root.after(100, update_table)
    root.mainloop()

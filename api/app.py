import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace

fontSize = 10

def create_grid(canvas):
    w = canvas.winfo_reqwidth() - 6  # Get current width of canvas
    h = canvas.winfo_reqheight() - 6  # Get current height of canvas
    print(w, h)
    canvas.delete('grid_line')  # Will only remove the grid_line
    # Creates all vertical lines at intevals of 100
    for i in range(0, w * 2, 100):
        canvas.create_line([(i, 0), (i, h * 2)], tag='grid_line')
    # Creates all horizontal lines at intevals of 100
    for i in range(0, h * 2, 100):
        canvas.create_line([(0, i), (w * 2, i)], tag='grid_line')
    canvas.create_line([(0, 1000), (w * 2, 1000)], tag='grid_line')
    canvas.create_line([(1000, 0), (1000, h * 2)], tag='grid_line')

def gui(frame, queue, Messages):
    control_panel = tk.PanedWindow(frame, bg="#d2d6d6")
    control_panel.grid(row=0, column=0, pady=15)
    label = tk.StringVar()
    label.set("Control Panel")
    tk.Label(control_panel, bg="#d2d6d6", textvariable=label).grid(row=0, column=1, pady=5)
    startbtn = tk.Button(control_panel, text="SIMULATE", command=lambda: queue.put(Messages.CLICK))
    startbtn.grid(row=1, column=0, pady=5, ipady=10, ipadx=10)
    nodeBtn = tk.Button(control_panel, text="STOP", command=lambda: queue.put(Messages.STOP))
    nodeBtn.grid(row=1, column=2, pady=5, ipady=10, ipadx=25)

    panel = tk.PanedWindow(frame)
    panel.grid(row=1, column=0, sticky="nsew", padx=200, pady=50)

    canvas = tk.Canvas(panel, width=500, height=500, highlightbackground="black")
    xsb = tk.Scrollbar(panel, orient="horizontal", command=canvas.xview)
    ysb = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas.configure(scrollregion=(0, 0, 1000, 1000))

    xsb.grid(row=2, column=0, sticky="ew")
    ysb.grid(row=1, column=1, sticky="ns")
    canvas.grid(row=1, column=0, sticky="nsew")

    global fontSize
    frame.fontSize = fontSize

    create_grid(canvas)

    node_panel = tk.PanedWindow(panel)
    node_panel.grid(row=1, column=2, sticky="nsew")

    panel1 = tk.PanedWindow(node_panel)
    panel1.grid(row=0, column=0)

    panel2 = tk.PanedWindow(node_panel)
    panel2.grid(row=1, column=0, pady=20)

    variable = tk.StringVar()

    menu = ttk.Combobox(panel1, state="readonly", width=25, textvariable=variable)
    menu.grid(row=0, column=0)

    dataLabel = tk.Label(panel2, text="Test", bg="yellow")
    dataLabel.grid(row=0, column=0, sticky="nsew")

    return SimpleNamespace(label=dataLabel, canvas=canvas, panel=panel, menu=menu)
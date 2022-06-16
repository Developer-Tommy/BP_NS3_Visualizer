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

def gui(frame, queue):
    control_panel = tk.PanedWindow(frame, bg="#d2d6d6")
    control_panel.grid(row=0, column=0, sticky="nw", padx=5)

    file_button = tk.Button(control_panel, text="File", command=lambda: queue.put("FILE"))
    file_button.grid(row=0, column=0, pady=5, ipady=10, ipadx=10)

    start_button = tk.Button(control_panel, text="START", command=lambda: queue.put("START"))
    start_button.grid(row=0, column=2, pady=5, ipady=10, ipadx=25)

    stop_button = tk.Button(control_panel, text="STOP", command=lambda: queue.put("STOP"))
    stop_button.grid(row=0, column=3, pady=5, ipady=10, ipadx=25)

    fast = tk.Label(control_panel, text="fast", bg="#d2d6d6")
    fast.grid(row=0, column=4, pady=5, ipady=8, ipadx=10)

    slider = ttk.Scale(control_panel, from_=0.0, to=1.0, orient='horizontal', value=0.5, length=150)
    slider.grid(row=0, column=5)

    slow = tk.Label(control_panel, text="slow", bg="#d2d6d6")
    slow.grid(row=0, column=6, pady=5, ipady=8, ipadx=10)

    time_label = tk.Label(control_panel, text="0.0", bg="black", fg="white", width=10)
    time_label.grid(row=0, column=7, pady=5, ipady=8, ipadx=10)

    panel = tk.PanedWindow(frame)
    panel.grid(row=1, column=0, sticky="nsew", padx=5)

    canvas = tk.Canvas(panel, width=700, height=700, highlightbackground="black")
    xsb = tk.Scrollbar(panel, orient="horizontal", command=canvas.xview)
    ysb = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas.configure(scrollregion=(0, 0, 1000, 1000))

    xsb.grid(row=2, column=0, sticky="ew")
    ysb.grid(row=1, column=1, sticky="ns")
    canvas.grid(row=1, column=0, sticky="nsew")

    global fontSize
    frame.fontSize = fontSize

    # create_grid(canvas)

    node_panel = tk.PanedWindow(panel)
    node_panel.grid(row=1, column=2, sticky="nsew")

    panel1 = tk.PanedWindow(node_panel)
    panel1.grid(row=0, column=0)

    panel2 = tk.PanedWindow(node_panel)
    panel2.grid(row=1, column=0, pady=30)

    variable = tk.StringVar()

    menu = ttk.Combobox(panel1, state="readonly", width=30, textvariable=variable)
    menu.grid(row=0, column=0, pady=10)

    dataLabel = tk.Label(panel2)
    dataLabel.grid(row=0, column=0, sticky="nsew", ipadx=20, ipady=20)

    return SimpleNamespace(slider=slider, label=dataLabel, canvas=canvas, panel=panel, panel2=panel2, menu=menu, time=time_label)


def draw_communication(srcX, srcY, dstX, dstY, canvas, color, dash):
    if dash:
        arrow = canvas.create_line(srcX, srcY, dstX, dstY, arrow=tk.LAST, fill=color, width=4, dash=(5,3))
    else:
        arrow = canvas.create_line(srcX, srcY, dstX, dstY, arrow=tk.LAST, fill=color, width=4)
    return arrow

def draw_connection(srcX, srcY, dstX, dstY, canvas):
    canvas.create_line(srcX, srcY, dstX, dstY, fill="black", width=2)

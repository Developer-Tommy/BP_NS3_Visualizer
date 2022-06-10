import tkinter as tk
from queue import Queue
from threading import Thread
from api import *
import Logic as logic


# def onObjectClick(event, node, label):
#     print(node)
#     label.config(text="")
#     label.config(text=node.data[0].id)
#     print(node.data[0].id)
#     print('Got object click', event.x, event.y)
#     print(event.widget.find_closest(event.x, event.y))
#     item = event.widget.find_closest(event.x, event.y)[0]
#     tags = event.widget.gettags(item)
#     print(tags)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("950x800")
    root.title("Visualiser")
    queue = Queue()
    frame = tk.Frame(root, bg="#d2d6d6")
    frame.pack(fill="both", expand=True)
    guiRef = app.gui(frame, queue)
    control_thread = Thread(target=logic.updateCycle, args=(guiRef, queue))
    simulation_thread = Thread(target=logic.sim, args=(guiRef,))
    control_thread.daemon = True
    control_thread.start()
    simulation_thread.daemon = True
    simulation_thread.start()
    tk.mainloop()




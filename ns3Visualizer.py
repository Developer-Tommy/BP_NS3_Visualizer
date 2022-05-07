import tkinter as tk
from queue import Queue
from enum import Enum
from threading import Thread
from api import *
from utils import *
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


class Messages(Enum):
    FILE = 0,
    START = 0,
    STOP = 0



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x1000")
    root.title("Visualiser")
    queue = Queue()
    frame = tk.Frame(root, bg="#d2d6d6")
    frame.pack(fill="both", expand=True)
    guiRef = app.gui(frame, queue, Messages)
    t = Thread(target=logic.updateCycle, args=(guiRef, queue, Messages))
    t.daemon = True
    t.start()
    tk.mainloop()

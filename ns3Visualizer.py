import tkinter as tk
from queue import Queue
from enum import Enum
from threading import Thread
from api import *
from utils import *

class Messages(Enum):
    CLICK = 0,
    STOP = 0


storeNodes = list()


def findNode(menu, canvas):
    val = 0
    for node in storeNodes:
        canvas.itemconfig(node.node, fill=node.color)
        if node.id == int(menu.get()):
            canvas.itemconfig(node.node, fill="blue")
            val = node
    return val


def checkNode(menu, label, canvas):
    node = findNode(menu, canvas)
    label.configure(text=node.printNode())



def updateCycle(guiRef, queue):
    while True:
        msg = queue.get()
        if msg == Messages.CLICK:
            my_canvas = guiRef.canvas
            my_menu = guiRef.menu
            my_label = guiRef.label
            parser.readXML(my_canvas, storeNodes)
            for node in storeNodes:
                my_menu['values'] = tuple(list(my_menu['values']) + [str(node.id)])
            my_menu.current(0)
            my_menu.bind("<<ComboboxSelected>>", lambda event: checkNode(my_menu, my_label, my_canvas))

        elif msg == Messages.STOP:
            my_canvas = guiRef.canvas
            my_canvas.bind("<ButtonPress-1>", lambda event: move.move_start(event, my_canvas))
            my_canvas.bind("<B1-Motion>", lambda event: move.move_move(event, my_canvas))

            my_canvas.bind("<ButtonPress-2>", lambda event: move.pressed2(event, my_canvas))
            my_canvas.bind("<Motion>", lambda event: move.move_move2(event, my_canvas))

            # linux scroll
            my_canvas.bind("<Button-4>", lambda event: zoom.zoomerP(event, my_canvas))
            my_canvas.bind("<Button-5>", lambda event: zoom.zoomerM(event, my_canvas))
            # windows scroll
            my_canvas.bind("<MouseWheel>", lambda event: zoom.zoomer(event, my_canvas))



def onObjectClick(event, node, label):
    print(node)
    label.config(text="")
    label.config(text=node.data[0].id)
    print(node.data[0].id)
    print('Got object click', event.x, event.y)
    print(event.widget.find_closest(event.x, event.y))
    item = event.widget.find_closest(event.x, event.y)[0]
    tags = event.widget.gettags(item)
    print(tags)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x1000")
    root.title("Visualiser")
    queue = Queue()
    frame = tk.Frame(root, bg="#d2d6d6")
    frame.pack(fill="both", expand=True)
    guiRef = app.gui(frame, queue, Messages)
    t = Thread(target=updateCycle, args=(guiRef, queue,))
    t.daemon = True
    t.start()
    tk.mainloop()

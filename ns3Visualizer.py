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

def checkNode(mycanvas, label):
    for nodeHover in storeNodes:
        print("in= ")
        print(nodeHover)
        node = nodeHover
        mycanvas.tag_bind(nodeHover.node, '<ButtonPress-1>', lambda event: onObjectClick(event, node, label))


def updateCycle(guiRef, queue):
    while True:
        msg = queue.get()
        if msg == Messages.CLICK:
            mycanvas = guiRef.canvas
            parser.readXML(mycanvas, storeNodes)
        elif msg == Messages.STOP:
            print("STOP")
            if storeNodes:
                print(storeNodes[0].data[1].channel)
            mycanvas = guiRef.canvas
            mycanvas.bind("<ButtonPress-1>", lambda event: move.move_start(event, mycanvas))
            mycanvas.bind("<B1-Motion>", lambda event: move.move_move(event, mycanvas))

            mycanvas.bind("<ButtonPress-2>", lambda event: move.pressed2(event, mycanvas))
            mycanvas.bind("<Motion>", lambda event: move.move_move2(event, mycanvas))

            # linux scroll
            mycanvas.bind("<Button-4>", lambda event: zoom.zoomerP(event, mycanvas))
            mycanvas.bind("<Button-5>", lambda event: zoom.zoomerM(event, mycanvas))
            # windows scroll
            mycanvas.bind("<MouseWheel>", lambda event: zoom.zoomer(event, mycanvas))
            mycanvas = guiRef.canvas
            label = guiRef.label
            checkNode(mycanvas, label)



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
    root.geometry("1000x1000")
    root.title("Visualiser")
    queue = Queue()
    frame = tk.Frame(root, bg="#d2d6d6")
    frame.pack(fill="both", expand=True)
    guiRef = app.gui(frame, queue, Messages)
    t = Thread(target=updateCycle, args=(guiRef, queue,))
    t.daemon = True
    t.start()
    tk.mainloop()

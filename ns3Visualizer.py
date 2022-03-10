import tkinter as tk
import xml.dom.minidom
from types import SimpleNamespace
from queue import Queue
from enum import Enum
from threading import Thread


class Messages(Enum):
    CLICK = 0


class Node:
    def __init__(self, canvas, color, posx, posy):
        print("test init")
        self.canvas = canvas
        self.color = color
        self.posx = posx
        self.posy = posy
        #canvas.create_oval(10, 10, 40, 40, outline="black", fill=self.color, width=1)
        canvas.create_oval(self.posx-15, self.posy-15, self.posx+15, self.posy+15, outline="black", fill=self.color, width=1)


    def moveNode(self, posx, posy):
        print("move node")
        print(posx, posy)
        self.canvas.move(self, posx, posy)


def readXML(myCanvas):
    doc = xml.dom.minidom.parse("ns3.xml")
    nodes = doc.getElementsByTagName("node")
    nu = doc.getElementsByTagName("nu")
    print("%d nodes: " % nodes.length)
    count = 0
    storeNodes = list()
    for node in nodes:
        posX = int(node.getAttribute("locX"))
        posY = int(node.getAttribute("locY"))

        rval = int(nu[count].getAttribute("r"))
        gval = int(nu[count].getAttribute("g"))
        bval = int(nu[count].getAttribute("b"))
        color = '#%02x%02x%02x' % (rval, gval, bval)
        print(color)

        #circlenode = myCanvas.create_oval(10, 10, 40, 40, outline="black", fill="green", width=1)
        circle = Node(myCanvas, color, posX, posY)
        storeNodes.append(circle)
        #circle.moveNode(posX, posY)
        #myCanvas.move(circlenode, posX, posY)
        count = count + 1


def updateCycle(guiRef, queue):
    while True:
        msg = queue.get()
        if msg == Messages.CLICK:
            mycanvas = guiRef.canvas
            readXML(mycanvas)


def create_grid(canvas):
    w = canvas.winfo_reqwidth()-6 # Get current width of canvas
    h = canvas.winfo_reqheight()-6 # Get current height of canvas
    print(w,h)
    canvas.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, 100):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, 100):
        canvas.create_line([(0, i), (w, i)], tag='grid_line')



def gui(root, queue):
    label = tk.StringVar()
    label.set("Control Panel")
    tk.Label(root, textvariable=label).pack()
    startbtn = tk.Button(root, text="SIMULATE", command=lambda: queue.put(Messages.CLICK))
    startbtn.pack(ipadx=20, ipady=10)
    canvas = tk.Canvas(root, width=500, height=500, highlightbackground="black")
    canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, ipadx=100, ipady=100)
    create_grid(canvas)
    return SimpleNamespace(label=label, canvas=canvas)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Visualiser")
    queue = Queue()
    guiRef = gui(root, queue)
    t = Thread(target=updateCycle, args=(guiRef, queue,))
    t.daemon = True
    t.start()
    tk.mainloop()

import tkinter as tk
import xml.dom.minidom
from types import SimpleNamespace
from queue import Queue
from enum import Enum
from threading import Thread

pressed = False
fontSize = 10

class Messages(Enum):
    CLICK = 0,
    STOP = 0


class Node:
    def __init__(self, id, canvas, color, posx, posy, data):
        self.id = id
        self.canvas = canvas
        self.color = color
        self.posx = posx
        self.posy = posy
        self.data = data
        self.node = canvas.create_oval(self.posx+85, self.posy+85, self.posx+115, self.posy+115, outline="black", fill=self.color, width=1)


    def moveNode(self, posx, posy):
        print("move node")
        print(posx, posy)
        self.canvas.move(self, posx, posy)


storeNodes = list()

class Data:
    def __init__(self, id, ip, channel):
        self.id = id
        self.ip = ip
        self.channel = channel

def readXML(myCanvas):
    doc = xml.dom.minidom.parse("ns3.xml")
    nodes = doc.getElementsByTagName("node")
    nu = doc.getElementsByTagName("nu")

    addresNodes = doc.getElementsByTagName("nonp2plinkproperties")

    print("%d IP adresses: " %addresNodes.length)

    address = []
    allAddresses = []
    index = 0

    for a in addresNodes:
        if int(a.getAttribute("id")) != index:
            allAddresses.append(address)
            address = []
            index = index + 1
        if int(a.getAttribute("id")) == index:
            data = Data(int(a.getAttribute("id")), a.getAttribute("ipAddress"), a.getAttribute("channelType"))
            address.append(data)

    allAddresses.append(address)

    print(allAddresses)

    count = 0

    for node in nodes:
        color = '#%02x%02x%02x' % (int(nu[count].getAttribute("r")), int(nu[count].getAttribute("g")), int(nu[count].getAttribute("b")))
        circle = Node(int(node.getAttribute("id")), myCanvas, color, int(node.getAttribute("locX")), int(node.getAttribute("locY")), allAddresses[count])
        storeNodes.append(circle)
        count = count + 1

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
            readXML(mycanvas)
            print("out= ")
            print(storeNodes[0])

        elif msg == Messages.STOP:
            print("STOP")
            if storeNodes:
                print(storeNodes[0].data[1].channel)
            mycanvas = guiRef.canvas
            mycanvas.bind("<ButtonPress-1>", lambda event: move_start(event, mycanvas))
            mycanvas.bind("<B1-Motion>", lambda event: move_move(event, mycanvas))

            mycanvas.bind("<ButtonPress-2>", lambda event: pressed2(event, mycanvas))
            mycanvas.bind("<Motion>", lambda event: move_move2(event, mycanvas))

            # linux scroll
            mycanvas.bind("<Button-4>", lambda event: zoomerP(event, mycanvas))
            mycanvas.bind("<Button-5>", lambda event: zoomerM(event, mycanvas))
            # windows scroll
            mycanvas.bind("<MouseWheel>", lambda event: zoomer(event, mycanvas))
            mycanvas = guiRef.canvas
            label = guiRef.label
            checkNode(mycanvas, label)



def create_grid(canvas):
    w = canvas.winfo_reqwidth()-6 # Get current width of canvas
    h = canvas.winfo_reqheight()-6 # Get current height of canvas
    print(w, h)
    canvas.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w*2, 100):
        canvas.create_line([(i, 0), (i, h*2)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h*2, 100):
        canvas.create_line([(0, i), (w*2, i)], tag='grid_line')

    canvas.create_line([(0, 1000), (w*2, 1000)], tag='grid_line')
    canvas.create_line([(1000, 0), (1000, h*2)], tag='grid_line')

#move
def move_start(event, canvas):
    canvas.scan_mark(event.x, event.y)

def move_move(event, canvas):
    canvas.scan_dragto(event.x, event.y, gain=1)

#move
def pressed2(event, canvas):
    global pressed
    pressed = not pressed
    canvas.scan_mark(event.x, event.y)

def move_move2(event, canvas):
    if pressed:
        canvas.scan_dragto(event.x, event.y, gain=1)

#windows zoom
def zoomer(event, canvas):
    global fontSize
    if (event.delta > 0):
        canvas.scale("all", event.x, event.y, 1.1, 1.1)
        fontSize = fontSize * 1.1
    elif (event.delta < 0):
        canvas.scale("all", event.x, event.y, 0.9, 0.9)
        fontSize = fontSize * 0.9
    canvas.configure(scrollregion = canvas.bbox("all"))
    for child_widget in canvas.find_withtag("text"):
        canvas.itemconfigure(child_widget, font=("Helvetica", int(fontSize)))

#linux zoom
def zoomerP(event, canvas):
    canvas.scale("all", event.x, event.y, 1.1, 1.1)
    canvas.configure(scrollregion=canvas.bbox("all"))
def zoomerM(event, canvas):
    canvas.scale("all", event.x, event.y, 0.9, 0.9)
    canvas.configure(scrollregion=canvas.bbox("all"))

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

def gui(frame, queue):
    label = tk.StringVar()
    label.set("Control Panel")
    tk.Label(frame, textvariable=label).grid(row=1, column=0)
    startbtn = tk.Button(frame, text="SIMULATE", command=lambda: queue.put(Messages.CLICK))
    startbtn.grid(row=2, column=0)
    nodeBtn = tk.Button(frame, text="STOP", command=lambda: queue.put(Messages.STOP))
    nodeBtn.grid(row=3, column=0)

    panel = tk.PanedWindow(frame)
    panel.grid(row=4, column=0, sticky="nsew", padx=200, pady=100)

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

    dataLabel = tk.Label(panel, text="Test", bg="yellow")
    dataLabel.grid(row=1, column=2)

    return SimpleNamespace(label=dataLabel, canvas=canvas)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1000x1000")
    root.title("Visualiser")
    queue = Queue()
    frame = tk.Frame(root, bg="#d2d6d6")
    frame.pack(fill="both", expand=True)
    guiRef = gui(frame, queue)
    t = Thread(target=updateCycle, args=(guiRef, queue,))
    t.daemon = True
    t.start()
    tk.mainloop()

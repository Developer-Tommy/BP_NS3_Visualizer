from tkinter import filedialog
import Logic as logic
from api import *

class Data:
    def __init__(self, id, ip, channel):
        self.id = id
        self.ip = ip
        self.channel = channel

    def printData(self):
        print("ip: ", self.ip, "channel: ", self.channel)
        return "\n" + "ip: " + str(self.ip) + "\n" + "channel: " + str(self.channel) + "\n"

class Node:
    def __init__(self, id, canvas, posx, posy, color, desc, data):
        self.id = id
        self.canvas = canvas
        self.posx = posx
        self.posy = posy
        self.data = data
        self.desc = desc
        self.color = color
        self.node = canvas.create_oval(self.posx, self.posy, self.posx, self.posy,
                                       outline="black", fill=self.color, width=1)
    # setter method
    def set_color(self, new_color):
        self.color = new_color
        self.canvas.itemconfig(self.node, fill=new_color)

    def set_pos(self, new_posX, new_posY):
        self.posx = new_posX
        self.posy = new_posY
        self.canvas.move(self.node, new_posX, new_posY)

    def set_size(self, new_width, new_height):
        new_width = new_width * 2
        new_height = new_height * 2
        x0, y0, x1, y1 = self.canvas.coords(self.node)
        self.canvas.coords(self.node, x0-new_width, y0-new_height, x1+new_width, y1+new_height)
        x0, y0, x1, y1 = self.canvas.coords(self.node)
        print(x0, y0, x1, y1)
        print("\n")

    def set_description(self, new_desc):
        print(new_desc)
        self.desc = new_desc

    def printNode(self):
        print("id: ", self.id, " start posX: ", self.posx + 85, " start posY: ", self.posy + 85, " end posX: ", self.posx + 115, " end posY: ", self.posy + 115)
        node = "id: " + str(self.id) + "\n" + "Desc: " + str(self.desc) + "\n " + "start posX: " + str(self.posx) + "\n" + "start posY: " + str(self.posy) + "\n" + "end posX: " + str(self.posx) + "\n" + "end posY: " + str(self.posy) + "\n"
        for d in self.data:
            node += d.printData()
        return node


def readXML(myCanvas, storeNodes, doc):
    nodes = doc.getElementsByTagName("node")
    nu = doc.getElementsByTagName("nu")

    addresNodes = doc.getElementsByTagName("nonp2plinkproperties")
    point_to_point = doc.getElementsByTagName("link")


    address = []
    allAddresses = []
    index = 0

    for a in addresNodes:
        if int(a.getAttribute("id")) != index:
            address.pop()
            allAddresses.append(address)
            address = []
            index = index + 1
        if int(a.getAttribute("id")) == index:
            data = Data(int(a.getAttribute("id")), a.getAttribute("ipAddress"), a.getAttribute("channelType"))
            address.append(data)

    address.pop()
    allAddresses.append(address)

    count = 0

    #Node Updates check 
    for node in nodes:
        circle = Node(int(node.getAttribute("id")), myCanvas, float(node.getAttribute("locX")), float(node.getAttribute("locY")), "red", "", allAddresses[count])
        for n in nu:
            if int(n.getAttribute("id")) == int(node.getAttribute("id")):
                if float(n.getAttribute("t")) > 0.0:
                    break
                node_update(circle, n)
        storeNodes.append(circle)
        count = count + 1

    for connect in point_to_point:
        src = nodeData.findNode_by_id(int(connect.getAttribute("fromId")), storeNodes)
        dst = nodeData.findNode_by_id(int(connect.getAttribute("toId")), storeNodes)
        new_data_src = Data(src.id, connect.getAttribute("fd"), "Point-To-Point")
        new_data_dst = Data(dst.id, connect.getAttribute("td"), "Point-To-Point")
        src.data.append(new_data_src)
        dst.data.append(new_data_dst)
        srcx0, srcy0, srcx1, srcy1 = myCanvas.coords(src.node)
        dstx0, dsty0, dstx1, dsty1 = myCanvas.coords(dst.node)
        app.draw_connection(logic.cords(srcx0, srcx1), logic.cords(srcy0, srcy1), logic.cords(dstx0, dstx1), logic.cords(dsty0, dsty1),myCanvas)


def node_update(node, update):
    if update.getAttribute("p") == "c":
        color = '#%02x%02x%02x' % (int(update.getAttribute("r")), int(update.getAttribute("g")), int(update.getAttribute("b")))
        node.set_color(color)
    elif update.getAttribute("p") == "s":
        node.set_size(int(update.getAttribute("w")), int(update.getAttribute("h")))
        print("teraz sme v setsize")
    elif update.getAttribute("p") == "p":
        node.set_pos(float(update.getAttribute("x")), float(update.getAttribute("y")))
    elif update.getAttribute("p") == "d":
        node.set_description(update.getAttribute("descr"))
    else:
        return

def file_open():
    path = filedialog.askopenfilename(filetypes=[("SEM readable files", ( ".xml")), ("SEM XML files", ("*.xml", ".sem")), ("All files", ".*")])
    return path






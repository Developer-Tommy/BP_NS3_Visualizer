import xml.dom.minidom

class Data:
    def __init__(self, id, ip, channel):
        self.id = id
        self.ip = ip
        self.channel = channel

class Node:
    def __init__(self, id, canvas, color, posx, posy, data):
        self.id = id
        self.canvas = canvas
        self.color = color
        self.posx = posx
        self.posy = posy
        self.data = data
        self.node = canvas.create_oval(self.posx + 85, self.posy + 85, self.posx + 115, self.posy + 115,
                                       outline="black", fill=self.color, width=1)        

def readXML(myCanvas, storeNodes):
    doc = xml.dom.minidom.parse("ns3.xml")
    nodes = doc.getElementsByTagName("node")
    nu = doc.getElementsByTagName("nu")

    addresNodes = doc.getElementsByTagName("nonp2plinkproperties")

    print("%d IP adresses: " % addresNodes.length)

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
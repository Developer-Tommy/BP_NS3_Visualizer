def findNode(menu, canvas, storeNodes):
    val = 0
    for node in storeNodes:
        canvas.itemconfig(node.node, fill=node.color)
        if node.id == int(menu.get()):
            canvas.itemconfig(node.node, fill="blue")
            val = node
    return val


def checkNode(menu, label, canvas, panel, nodes):
    node = findNode(menu, canvas, nodes)
    panel.configure(background="black", borderwidth=2)
    label.configure(text=node.printNode())
from queue import Queue
from api import *
from utils import *
import xml.dom.minidom
from utils.parser import file_open
from time import sleep
from random import randint
myFlag = False

storeNodes = list()
source_document = xml.dom.minidom
simulation = []
wifi_communication = []
update_nodes_positions = []
line_counter = 0
end_of_file = 0
is_paused = True

def updateCycle(guiRef, queue):
    global is_paused
    global simulation
    global wifi_communication
    global update_nodes_positions
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

    while True:
        msg = queue.get()
        
        print(msg)
        if msg == "FILE":
            my_menu = guiRef.menu
            my_label = guiRef.label
            my_panel2 = guiRef.panel2
            source_document = xml.dom.minidom.parse(file_open())
            parser.readXML(my_canvas, storeNodes, source_document)
            for node in storeNodes:
                my_menu['values'] = tuple(list(my_menu['values']) + [str(node.id)])
            my_menu.current(0)
            my_menu.bind("<<ComboboxSelected>>", lambda event: nodeData.checkNode(my_menu, my_label, my_canvas, my_panel2, storeNodes))

            # guiRef.frame.start_button.enableButton.config(state = 'active')
            # simulation = source_document.getElementsByTagName("p")
            # simulation = source_document.getElementsByTagName("wpr")
            # for i in simulation:
            #     print("toto je udalost " , i)

            simulation = source_document.getElementsByTagName("p")
            wifi_communication = source_document.getElementsByTagName("wpr")

            for wifi in source_document.getElementsByTagName("pr"):
                simulation.append(wifi)
            for nu in source_document.getElementsByTagName("nu"):
                if float(nu.getAttribute("t")) > 0.0:
                    update_nodes_positions.append(nu)
                    print("toto je udalost " , nu)

            simulation = quicksort(simulation)

        elif msg == "START":
            is_paused = False

        elif msg == "STOP":
            is_paused = True
            

def load_simulation_frame(simulation_frame, next_simulation_frame, wifi_sent_to, storeNodes, canvas, time_label, arrow_queue):
        while not arrow_queue.empty():
                canvas.delete(arrow_queue.get())
        source_node = nodeData.findNode_by_id(simulation_frame.getAttribute("fId"), storeNodes)
        srcx0, srcy0, srcx1, srcy1 = canvas.coords(source_node.node)
        if simulation_frame.tagName == "pr":
            uId = int(simulation_frame.getAttribute("uId"))
            for wifi in wifi_sent_to:
                if int(wifi.getAttribute("uId")) == uId:
                    destination_node = nodeData.findNode_by_id(wifi.getAttribute("tId"), storeNodes)
                    dstx0, dsty0, dstx1, dsty1 = canvas.coords(destination_node.node)
                    time_label.config(text=float(simulation_frame.getAttribute("fbTx")))
                    arrow_queue.put(app.draw_communication(cords(srcx0, srcx1), cords(srcy0, srcy1), cords(dstx0, dstx1),cords(dsty0, dsty1), canvas, "blue", True))

        if simulation_frame.tagName == "p":
            destination_node = nodeData.findNode_by_id(simulation_frame.getAttribute("tId"), storeNodes)
            dstx0, dsty0, dstx1, dsty1 = canvas.coords(destination_node.node)
            time_label.config(text=float(simulation_frame.getAttribute("fbTx")))
            arrow_queue.put(app.draw_communication(cords(srcx0,srcx1), cords(srcy0,srcy1), cords(dstx0,dstx1), cords(dsty0,dsty1), canvas, "green", False))

        if next_simulation_frame != 0:
            for nu in update_nodes_positions:
                if float(simulation_frame.getAttribute("fbTx")) < float(nu.getAttribute("t")) < float(
                        next_simulation_frame.getAttribute("fbTx")):
                    updated_node = nodeData.findNode_by_id(nu.getAttribute("id"), storeNodes)
                    parser.node_update(updated_node, nu)
                    print("new position of runner")


def sim(guiRef):
    global is_paused
    global line_counter
    arrow_queue = Queue()
    while True:
        if is_paused:
            # print('STOP Pressed')
            sleep(0.5)

        elif not is_paused and len(simulation)-1 > line_counter:
            
            load_simulation_frame(simulation[line_counter], simulation[line_counter+1], wifi_communication, storeNodes, guiRef.canvas, guiRef.time, arrow_queue)
            line_counter += 1
            # print('START Pressed')
            sleep(0.5)
        elif not is_paused and len(simulation)-1 == line_counter:
            load_simulation_frame(simulation[line_counter], 0, wifi_communication, storeNodes, guiRef.canvas, guiRef.time, arrow_queue)
            line_counter += 1
            # print('START Pressed')
            sleep(0.5)
        else:
            sleep(0.5)


def cords(x0, x1):
    x = (x0 + x1)/2
    return x

def quicksort(array):
    # If the input array contains fewer than two elements,
    # then return it as the result of the function
    if len(array) < 2:
        return array

    low, same, high = [], [], []

    # Select your `pivot` element randomly
    pivot = array[randint(0, len(array) - 1)]

    for item in array:
        # Elements that are smaller than the `pivot` go to
        # the `low` list. Elements that are larger than
        # `pivot` go to the `high` list. Elements that are
        # equal to `pivot` go to the `same` list.
        if float(item.getAttribute("fbTx")) < float(pivot.getAttribute("fbTx")):
            low.append(item)
        elif float(item.getAttribute("fbTx")) == float(pivot.getAttribute("fbTx")):
            same.append(item)
        elif float(item.getAttribute("fbTx")) > float(pivot.getAttribute("fbTx")):
            high.append(item)

    # The final result combines the sorted `low` list
    # with the `same` list and the sorted `high` list
    return quicksort(low) + same + quicksort(high)
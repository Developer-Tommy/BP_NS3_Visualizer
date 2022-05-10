from queue import Queue
from api import *
from utils import *
import xml.dom.minidom
from utils.parser import file_open
from time import sleep
myFlag = False

storeNodes = list()
source_document = xml.dom.minidom
simulation = []
line_counter = 0
is_paused = True

def updateCycle(guiRef, queue):
    global is_paused
    global simulation
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

        elif msg == "START":
            simulation = source_document.getElementsByTagName("p")
            is_paused = False

        elif msg == "STOP":
            is_paused = True
            

def load_simulation_frame(simulation_frame, storeNodes, canvas, arrow_queue):
        if not arrow_queue.empty():
                canvas.delete(arrow_queue.get())
        source_node = nodeData.findNode_by_id(simulation_frame.getAttribute("fId"), storeNodes)
        destination_node = nodeData.findNode_by_id(simulation_frame.getAttribute("tId"), storeNodes)
        srcx0, srcy0, srcx1, srcy1 = canvas.coords(source_node.node)
        dstx0, dsty0, dstx1, dsty1 = canvas.coords(destination_node.node)
        arrow_queue.put(app.draw_communication(cords(srcx0,srcx1), cords(srcy0,srcy1), cords(dstx0,dstx1), cords(dsty0,dsty1), canvas))


def sim(guiRef):
    global is_paused
    global line_counter
    arrow_queue = Queue()
    while True:
        if is_paused:
            # print('STOP Pressed')
            sleep(0.5)

        elif not is_paused and len(simulation) > line_counter:
            load_simulation_frame(simulation[line_counter], storeNodes, guiRef.canvas, arrow_queue)
            line_counter += 1
            # print('START Pressed')
            sleep(0.5)
        else:
            sleep(0.5)


def cords(x0, x1):
    x = (x0 + x1)/2
    return x
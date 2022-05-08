from api import *
from utils import *
import xml.dom.minidom
from utils.parser import file_open

storeNodes = list()
source_document = xml.dom.minidom
simulation = []
line_counter = 0
is_paused = False

def updateCycle(guiRef, queue):
    while True:
        msg = queue.get()
        print(msg)
        global is_paused
        if msg == "FILE":
            my_canvas = guiRef.canvas
            my_menu = guiRef.menu
            my_label = guiRef.label
            my_panel2 = guiRef.panel2
            source_document = xml.dom.minidom.parse(file_open())
            parser.readXML(my_canvas, storeNodes, source_document)
            for node in storeNodes:
                my_menu['values'] = tuple(list(my_menu['values']) + [str(node.id)])
            my_menu.current(0)
            my_menu.bind("<<ComboboxSelected>>", lambda event: nodeData.checkNode(my_menu, my_label, my_canvas, my_panel2, storeNodes))

            my_canvas.bind("<ButtonPress-1>", lambda event: move.move_start(event, my_canvas))
            my_canvas.bind("<B1-Motion>", lambda event: move.move_move(event, my_canvas))

            my_canvas.bind("<ButtonPress-2>", lambda event: move.pressed2(event, my_canvas))
            my_canvas.bind("<Motion>", lambda event: move.move_move2(event, my_canvas))

            # linux scroll
            my_canvas.bind("<Button-4>", lambda event: zoom.zoomerP(event, my_canvas))
            my_canvas.bind("<Button-5>", lambda event: zoom.zoomerM(event, my_canvas))
            # windows scroll
            my_canvas.bind("<MouseWheel>", lambda event: zoom.zoomer(event, my_canvas))

        elif msg == "START":
            my_canvas = guiRef.canvas
            is_paused = False

             # linux scroll
            my_canvas.unbind("<Button-4>")
            my_canvas.unbind("<Button-5>")
            # windows scroll
            my_canvas.unbind("<MouseWheel>")
            global line_counter
            simulation = source_document.getElementsByTagName("p")
            line_counter = load_simulation(simulation, storeNodes, my_canvas, line_counter)

        elif msg == "STOP":
            print(is_paused)
            my_canvas = guiRef.canvas
            is_paused = True
            print(is_paused)
            # linux scroll
            my_canvas.bind("<Button-4>", lambda event: zoom.zoomerP(event, my_canvas))
            my_canvas.bind("<Button-5>", lambda event: zoom.zoomerM(event, my_canvas))
            # windows scroll
            my_canvas.bind("<MouseWheel>", lambda event: zoom.zoomer(event, my_canvas))
            
        # elif msg == Messages.CLICK:
        #     my_canvas = guiRef.canvas
        #     my_menu = guiRef.menu
        #     my_label = guiRef.label
        #     my_panel2 = guiRef.panel2
        #     parser.readXML(my_canvas, storeNodes, source_document)
        #     for node in storeNodes:
        #         my_menu['values'] = tuple(list(my_menu['values']) + [str(node.id)])
        #     my_menu.current(0)
        #     my_menu.bind("<<ComboboxSelected>>", lambda event: nodeData.checkNode(my_menu, my_label, my_canvas, my_panel2, storeNodes))


def load_simulation(simulation, storeNodes, canvas, counter):
    for x in range(counter, len(simulation)):
        if is_paused:
            return x
        source_node = nodeData.findNode_by_id(simulation[x].getAttribute("fId"), storeNodes)
        destination_node = nodeData.findNode_by_id(simulation[x].getAttribute("tId"), storeNodes)
        app.draw_communication(source_node.posx, source_node.posy, destination_node.posx, destination_node.posy, canvas)
    return counter
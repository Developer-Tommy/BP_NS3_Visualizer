fontSize = 10

# windows zoom
def zoomer(event, canvas):
    global fontSize
    if (event.delta > 0):
        canvas.scale("all", event.x, event.y, 1.1, 1.1)
        fontSize = fontSize * 1.1
    elif (event.delta < 0):
        canvas.scale("all", event.x, event.y, 0.9, 0.9)
        fontSize = fontSize * 0.9
    canvas.configure(scrollregion=canvas.bbox("all"))
    for child_widget in canvas.find_withtag("text"):
        canvas.itemconfigure(child_widget, font=("Helvetica", int(fontSize)))


# linux zoom
def zoomerP(event, canvas):
    canvas.scale("all", event.x, event.y, 1.1, 1.1)
    canvas.configure(scrollregion=canvas.bbox("all"))


def zoomerM(event, canvas):
    canvas.scale("all", event.x, event.y, 0.9, 0.9)
    canvas.configure(scrollregion=canvas.bbox("all"))
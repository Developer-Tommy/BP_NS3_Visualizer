pressed = False

# move
def move_start(event, canvas):
    canvas.scan_mark(event.x, event.y)


def move_move(event, canvas):
    canvas.scan_dragto(event.x, event.y, gain=1)


# move
def pressed2(event, canvas):
    global pressed
    pressed = not pressed
    canvas.scan_mark(event.x, event.y)


def move_move2(event, canvas):
    if pressed:
        canvas.scan_dragto(event.x, event.y, gain=1)

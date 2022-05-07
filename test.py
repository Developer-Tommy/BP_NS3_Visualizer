import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2) # add space for buttons

x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))

class Example:

    steps = 200

    def __init__(self):
        self.step_index = 0
        self.timer = None

    def animate(self):
        print(self.step_index)
        # update the data
        line.set_ydata(np.sin(x + (2 * np.pi * self.step_index / self.steps)))
        self.step_index += 1
        plt.draw()        

        # stop if end of animation
        if self.step_index >= self.steps:
            self.timer = None
            return False

    def play(self, event):
        if not self.timer:
            # no current animation, start a new one.
            self.timer = fig.canvas.new_timer(interval=10)
            self.timer.add_callback(self.animate)
            self.step_index = 0
        self.timer.start()

    def pause(self, event):
        if not self.timer:
            return
        self.timer.stop()

ex = Example()
ax_pause = plt.axes([0.7, 0.05, 0.1, 0.075])
ax_play = plt.axes([0.81, 0.05, 0.1, 0.075])
pause_button = Button(ax_pause, 'Pause')
pause_button.on_clicked(ex.pause)
play_button = Button(ax_play, 'Play')
play_button.on_clicked(ex.play)

plt.show()
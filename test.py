from Tkinter import *
from BoardWidget import BoardWidget
from BoardController import BoardController, Transform
from Constants import Rotation

root = Tk()
root.title('Peanuts')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

t = Transform(mirror=True, rotation=Rotation.NONE, swap=True)
c = BoardController(transform=t)

c.setup_test_position()

b = BoardWidget(root, controller=c, width=500, height=500, background='white')

b.grid(row=0, column=0, sticky=W+E+N+S)

mainloop()

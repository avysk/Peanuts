"""
Helper to play with BoardWidget and BoardModel
"""

import Tkinter as T
from BoardWidget import BoardWidget
from BoardController import BoardController, Transform
from BoardModel import BoardModel
from Constants import Rotation
from random import randint

def main():
    """
    Setup demo position and run Tkinter.mainloop()
    """
    root = T.Tk()
    root.title('Peanuts')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    if randint(0, 1) > 0:
        swap = True
        print "White to move"
    else:
        swap = False
        print "Black to move"

    if randint(0, 1) > 0:
        mirror = True
    else:
        mirror = False

    rotation = {
            0: Rotation.NONE,
            1: Rotation.RIGHT,
            2: Rotation.LEFT,
            3: Rotation.BOTH}[randint(0, 3)]

    transform = Transform(mirror=mirror, rotation=rotation, swap=swap)
    model = BoardModel()

    controller = BoardController(model=model, transform=transform)

    board = BoardWidget(root, controller=controller, width=500, height=500,
            background='white')

    board.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)
    # FIXME
    board._resize()

    controller.open_collection('problems/')
    controller.next_problem()

    T.mainloop()

if __name__ == '__main__':
    main()

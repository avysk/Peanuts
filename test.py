"""
Helper to play with BoardWidget and BoardModel
"""

import Tkinter as T
from BoardWidget import BoardWidget
from BoardController import BoardController, Transform
from BoardModel import BoardModel
from Constants import Rotation
from os import listdir
from os.path import isfile, join
import random

def main():
    """
    Setup demo position and run Tkinter.mainloop()
    """
    root = T.Tk()
    root.title('Peanuts')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    if random.randint(0, 1) > 0:
        swap = True
        print "White to move"
    else:
        swap = False
        print "Black to move"

    if random.randint(0, 1) > 0:
        mirror = True
    else:
        mirror = False

    rotation = {
            0: Rotation.NONE,
            1: Rotation.RIGHT,
            2: Rotation.LEFT,
            3: Rotation.BOTH}[random.randint(0, 3)]

    transform = Transform(mirror=mirror, rotation=rotation, swap=swap)
    model = BoardModel()

    controller = BoardController(model=model, transform=transform)

    board = BoardWidget(root, controller=controller, width=500, height=500,
            background='white')

    board.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)


    probs = [f for f in listdir('problems/') if isfile(join('problems/', f))]
    l = len(probs)
    r = random.randint(0, l - 1)
    print "Problem", probs[r]
    f = open(join('problems/', probs[r]))
    model.setup_sgf(f.read())

    T.mainloop()

if __name__ == '__main__':
    main()

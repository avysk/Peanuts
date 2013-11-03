"""
Helper to play with BoardWidget and BoardModel
"""

import Tkinter as T
from BoardWidget import BoardWidget
from BoardController import BoardController, Transform
from BoardModel import BoardModel
from Constants import Rotation

def main():
    """
    Setup demo position and run Tkinter.mainloop()
    """
    root = T.Tk()
    root.title('Peanuts')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    #t = Transform(mirror=False, rotation=Rotation.NONE, swap=False)
    transform = Transform(mirror=True, rotation=Rotation.NONE, swap=True)
    model = BoardModel()
    model.setup_test_position()

    controller = BoardController(model=model, transform=transform)

    board = BoardWidget(root, controller=controller, width=500, height=500,
            background='white')

    board.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)

    T.mainloop()

if __name__ == '__main__':
    main()

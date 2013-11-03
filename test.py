from Tkinter import *
from BoardWidget import BoardWidget
from BoardController import BoardController, Transform
from BoardModel import BoardModel
from Constants import Rotation

def main():
    root = Tk()
    root.title('Peanuts')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    #t = Transform(mirror=False, rotation=Rotation.NONE, swap=False)
    t = Transform(mirror=True, rotation=Rotation.NONE, swap=True)
    m = BoardModel()
    m.setup_test_position()

    c = BoardController(model=m, transform=t)

    b = BoardWidget(root, controller=c, width=500, height=500, background='white')

    b.grid(row=0, column=0, sticky=W+E+N+S)

    mainloop()

if __name__ == '__main__':
    main()

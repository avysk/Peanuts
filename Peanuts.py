import Tkinter as T
import ttk as TT
from BoardController import BoardController
from BoardWidget import BoardWidget

def main():
    root0 = T.Tk()
    root0.title('Peanuts')

    root = TT.Frame(root0)
    root0.grid_columnconfigure(0, weight=1)
    root0.grid_rowconfigure(0, weight=1)
    root.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=0)
    root.grid_rowconfigure(0, weight=1)

    # Left frame
    left_frame = TT.Frame(root)
    left_frame.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)
    left_frame.grid_columnconfigure(0, weight=1)
    # Board height may be changed
    left_frame.grid_rowconfigure(0, weight=1)
    # Caption is of fixed height
    left_frame.grid_rowconfigure(1, weight=0)

    v_message = T.StringVar()
    controller = BoardController(v_message)
    board = BoardWidget(left_frame, controller=controller,
            width=500, height=500,
            background='yellow', highlightthickness=0,
            cursor='hand1')
    board.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)

    label_message = TT.Label(left_frame, textvariable=v_message)
    label_message.grid(row=1, column=0)

    # Right frame
    right_frame = TT.Frame(root)
    right_frame.grid(row=0, column=1, sticky=T.W+T.E+T.N+T.S)
    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_rowconfigure(0, weight=0)
    # Button box is resizable
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_rowconfigure(2, weight=0)

    next_button = TT.Button(right_frame, text='Next', command=controller.next_problem)
    next_button.grid(row=1, column=0, sticky=T.S)

    resizer = TT.Sizegrip(right_frame)
    resizer.grid(row=2, column=0, sticky=T.S+T.E)

    controller.open_collection('problems/')
    controller.next_problem()

    T.mainloop()

if __name__ == '__main__':
    main()

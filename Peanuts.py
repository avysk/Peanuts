# vim: set fileencoding=utf-8
import Tkinter as T
import tkMessageBox
import ttk as TT
import Image as I
import ImageTk as IT
from BoardController import BoardController
from BoardWidget import BoardWidget

def about():
    tkMessageBox.showinfo("About", u"Peanuts v1.0.0.\n© 2013, Alexey Vyskubov")

def preferences():
    tkMessageBox.showerror("Preferences", "Preferences are not implemented.",
            icon=tkMessageBox.ERROR)

def put_square_board(board, padding):
    """
    Put given board widget in the top left corner of padding frame and make
    sure it is always as big as possible but is a square.
    """
    def square_it(e, old_size={}):
        # This is horrible hack: old_size['size'] plays the role of static
        # variable in C; bypassing board.place when the size is the same helps
        # to do redraws during resizing reasonably fast
        right_size = min(e.width, e.height)
        if old_size.get('size') == right_size:
            print "no need"
            return
        else:
            old_size['size'] = right_size
        board.place(in_=padding, x=0, y=0, width=right_size, height=right_size)

    padding.bind('<Configure>', square_it)

def main():
    root0 = T.Tk()
    root0.title('Peanuts')
    root0.createcommand('tkAboutDialog', about)
    root0.createcommand('::tk::mac::ShowPreferences', preferences)

    m = T.Menu(root0)
    #m_apple = T.Menu(m, name='apple')
    m_help = T.Menu(m, name='help')
    #m.add_cascade(menu=m_apple)
    m.add_cascade(menu=m_help, label='Help')
    root0['menu'] = m

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

    # Let's create padding frame for the board
    padding = TT.Frame(left_frame, width=700, height=700)
    padding.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)

    v_message = T.StringVar()
    controller = BoardController(v_message)
    board = BoardWidget(left_frame, controller=controller,
            width=500, height=500,
            background='yellow', highlightthickness=0,
            cursor='hand1')

    # Now put the board in the padding frame
    put_square_board(board, padding)

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

    img = I.open('images/next.png')
    image_next = IT.PhotoImage(img)

    next_button = TT.Button(right_frame, image=image_next,
            command=controller.next_problem)
    next_button.grid(row=1, column=0, sticky=T.S)

    resizer = TT.Sizegrip(right_frame)
    resizer.grid(row=2, column=0, sticky=T.S+T.E)

    controller.open_collection('problems/')
    controller.next_problem()

    T.mainloop()

if __name__ == '__main__':
    main()

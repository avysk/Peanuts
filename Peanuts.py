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

    img = I.open('images/next.png')
    image_next = IT.PhotoImage(img)

    next_button = TT.Button(right_frame, image=image_next, command=controller.next_problem)
    next_button.grid(row=1, column=0, sticky=T.S)

    resizer = TT.Sizegrip(right_frame)
    resizer.grid(row=2, column=0, sticky=T.S+T.E)

    controller.open_collection('problems/')
    controller.next_problem()

    T.mainloop()

if __name__ == '__main__':
    main()

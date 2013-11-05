import Tkinter as T
from BoardController import BoardController
from BoardWidget import BoardWidget

def main():
    root = T.Tk()
    root.title('Peanuts')
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=0)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)

    v_message = T.StringVar()
    controller = BoardController(v_message)

    board = BoardWidget(root, controller=controller, width=500, height=500,
            background='white')
    board.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)

    label_message = T.Label(textvariable=v_message)
    label_message.grid(row=1, column=0)

    next_button = T.Button(root, text='Next', command=controller.next_problem)
    next_button.grid(row=1, column=1, sticky=T.S+T.E, padx=5, pady=10)

    controller.open_collection('problems/')
    controller.next_problem()

    T.mainloop()

if __name__ == '__main__':
    main()

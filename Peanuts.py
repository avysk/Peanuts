# vim: set fileencoding=utf-8
# Copyright (C) 2013 Alexey Vyskubov (alexey@ocaml.nl)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# The license is currently available on the Internet at:
#     http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
import sys
import Tkinter as T
import tkMessageBox
try:
    import ttk as TT
    def has_ttk():
        return not 'nottk' in sys.argv
except:
    def has_ttk():
        return False

try:
    import Image as I
    import ImageTk as IT
    def has_pil():
        return not 'nopil' in sys.argv
except:
    def has_pil():
        return False

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
    def square_it(static_vars):
        """
        Update board size.
        """
        assert(static_vars['queued'])
        # Allow to queue update again
        static_vars['queued'] = False
        desired = min(padding.winfo_width(), padding.winfo_height())
        if static_vars.get('size') == desired:
            # Do nothing if no changes in size
            return
        else:
            static_vars['size'] = desired
        board.place(in_=padding, x=0, y=0, width=desired, height=desired)

    def queue_update(e, static_vars={'queued': False, 'size': None}):
        """
        Queue update of the board size, but only if it's not already queued.
        """
        if not static_vars['queued']:
            static_vars['queued'] = True
            board.after_idle(square_it, static_vars)

    padding.bind('<Configure>', queue_update)

def create_root():
    """
    Create toplevel window, setup menus and fill toplevel with ttk frame.
    Return frame.
    """
    toplevel = T.Tk()
    toplevel.title('Peanuts')
    # Connect to Mac OS X system menu, "About" and "Preferences..."
    toplevel.createcommand('tkAboutDialog', about)
    toplevel.createcommand('::tk::mac::ShowPreferences', preferences)
    # Connect to Mac OS X system Help menu
    m = T.Menu(toplevel)
    m_help = T.Menu(m, name='help')
    m.add_cascade(menu=m_help, label='Help')
    # Add menu to the toplevel
    toplevel['menu'] = m
    # Configure grid geometry: allow resizing for inner widget
    toplevel.grid_columnconfigure(0, weight=1)
    toplevel.grid_rowconfigure(0, weight=1)
    root = TT.Frame(toplevel)
    root.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=0)
    root.grid_rowconfigure(0, weight=1)
    return root

def setup_left_frame(root):
    """
    Setup the left part of the interface: BoardWidget and message label. Return
    board controller.
    """
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
    # Setup board controller
    v_message = T.StringVar()
    controller = BoardController(v_message)
    # Setup board
    board = BoardWidget(left_frame, controller=controller, pil=has_pil(),
            width=500, height=500,
            background='yellow', highlightthickness=0,
            cursor='hand1')
    put_square_board(board, padding)
    # Setup message label
    label_message = TT.Label(left_frame, textvariable=v_message)
    label_message.grid(row=1, column=0)
    return controller

def setup_right_frame(root, controller, static_vars={'images':[]}):
    """
    Setup the right part of the interface.
    """
    right_frame = TT.Frame(root)
    right_frame.grid(row=0, column=1, sticky=T.W+T.E+T.N+T.S)
    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_rowconfigure(0, weight=0)
    # Button box is resizable
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_rowconfigure(2, weight=0)
    # Next problem button
    if has_pil():
        img = I.open('images/next.png')
        image_next = IT.PhotoImage(img)
        next_button = TT.Button(right_frame, image=image_next,
                command=controller.next_problem)
        # Tk bug workaround: images are garbage-collected if the only reference
        # belongs to a widget
        static_vars['images'].append(image_next)
    else:
        next_button = TT.Button(right_frame, text='Next problem',
                command=controller.next_problem)
    next_button.grid(row=1, column=0, sticky=T.S)
    # The nice widget to indicate the place to change window size
    resizer = TT.Sizegrip(right_frame)
    resizer.grid(row=2, column=0, sticky=T.S+T.E)

def main():
    if not has_ttk():
        tkMessageBox.showerror("No ttk",
                "No ttk module (Python/Tkinter too old?).\nPeanuts won't run.")
    else:
        root = create_root()
        controller = setup_left_frame(root)
        setup_right_frame(root, controller)
        controller.open_collection('problems/')
        controller.next_problem()
        if not has_pil():
            tkMessageBox.showwarning("No PIL", "No PIL library found.")
        T.mainloop()

if __name__ == '__main__':
    main()

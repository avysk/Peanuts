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

import tkinter as T
from tkinter import ttk as TT

from BoardWidget import BoardWidget

try:
    from PIL import Image as I
    from PIL import ImageTk as IT
    def _has_pil():
        return True
except:
    def _has_pil():
        return False

class UI(object):
    def __init__(self, about=None, preferences=None,
            controller=None,
            app_title='Peanuts',
            min_board_width=400,
            board_width=500,
            no_pil = False):
        self._controller = controller
        self._min_board_width = min_board_width
        self._has_pil = not no_pil and _has_pil()
        self._toplevel = self._create_toplevel(app_title, about, preferences)
        self._root = self._create_root()
        self._boardplacer = None
        self._images = []
        self._setup_left_frame(board_width)
        self._setup_right_frame()
        self._delta_x = 0
        self._delta_y = 0

    def run(self):
        self._toplevel.update()
        board_width = self._boardplacer.get_board_size()
        self._delta_x = self._toplevel.winfo_width() - board_width
        self._delta_y = self._toplevel.winfo_height() - board_width
        self._toplevel.minsize(self._min_board_width + self._delta_x,
                self._min_board_width + self._delta_y)
        T.mainloop()

    def _create_toplevel(self, title, about, preferences):
        """
        Create Tk toplevel and set up menus.
        Return toplevel.
        """
        toplevel = T.Tk()
        toplevel.title(title)
        # Connect to Mac OS X system menu, "About" and "Preferences..."
        toplevel.createcommand('tkAboutDialog', about)
        toplevel.createcommand('::tk::mac::ShowPreferences', preferences)
        m = T.Menu(toplevel)
        m_window = T.Menu(m)
        m.add_cascade(menu=m_window, label='Window')
        m_window.add_command(label='Fix size', command=self._fix_window_size)
        # Connect to Mac OS X system Help menu
        m_help = T.Menu(m, name='help')
        m.add_cascade(menu=m_help, label='Help')
        # Add menu to the toplevel
        toplevel['menu'] = m
        # Configure grid geometry: allow resizing of inner widget
        toplevel.grid_columnconfigure(0, weight=1)
        toplevel.grid_rowconfigure(0, weight=1)
        return toplevel

    def _create_root(self):
        """
        Create ttk frame filling self._topleve.
        Return frame.
        """
        root = TT.Frame(self._toplevel)
        root.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)
        root.grid_rowconfigure(0, weight=1)
        return root

    def _setup_left_frame(self, board_width):
        """
        Setup the left part of the interface: BoardWidget and message label.
        """
        left_frame = TT.Frame(self._root)
        left_frame.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)
        left_frame.grid_columnconfigure(0, weight=1)
        # Board height may be changed
        left_frame.grid_rowconfigure(0, weight=1)
        # Caption is of fixed height
        left_frame.grid_rowconfigure(1, weight=0)
        # Padding frame for the board
        padding = TT.Frame(left_frame, width=board_width, height=board_width)
        padding.grid(row=0, column=0, sticky=T.W+T.E+T.N+T.S)
        # Board
        board = BoardWidget(left_frame, controller = self._controller,
                pil=self._has_pil,
                width=board_width, height=board_width,
                background='yellow', highlightthickness=0,
                cursor='hand1')
        self._boardplacer = _BoardPlacer(board, padding)
        # Message label
        v_message = T.StringVar()
        self._controller.register_message_var(v_message)
        label_message = TT.Label(left_frame, textvariable=v_message)
        label_message.grid(row=1, column=0)

    def _setup_right_frame(self):
        """
        Setup the right part of the interface.
        """
        right_frame = TT.Frame(self._root)
        right_frame.grid(row=0, column=1, sticky=T.W+T.E+T.N+T.S)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=0)
        # Button box is resizable
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_rowconfigure(2, weight=0)
        # Button box
        buttonbox = TT.Frame(right_frame)
        buttonbox.grid(row=1, column=0, sticky=T.W+T.E+T.N+T.S)
        buttonbox.grid_columnconfigure(0, weight=1)
        buttonbox.grid_rowconfigure(0, weight=1)
        buttonbox.grid_rowconfigure(1, weight=1)
        # Next problem button
        image_next = None
        if self._has_pil:
            img = I.open('images/next.gif')
            image_next = IT.PhotoImage(img)
            # Tk bug workaround: images are garbage-collected if the only
            # reference belongs to a widget
            self._images.append(image_next)
        next_button = TT.Button(buttonbox,
                image=image_next, text='Next problem',
                compound=T.BOTTOM,
                takefocus=False,
                command=self._controller.next_problem)
        next_button.grid(row=1, column=0, sticky=T.S)
        # A nice widget to indicate the place to change window size
        resizer = TT.Sizegrip(right_frame)
        resizer.grid(row=2, column=0, sticky=T.S+T.E)

    def _fix_window_size(self):
        board_size = self._boardplacer.get_board_size()
        width = str(board_size + self._delta_x)
        height = str(board_size + self._delta_y)
        self._toplevel.geometry("%sx%s" % (width, height))


class _BoardPlacer(object):
    """
    Put given board widget in the top left corner of the padding frame and
    make sure it is always as big as possible but is a square.
    """
    def __init__(self, board, padding):
        self._board = board
        self._padding = padding
        self._queued = False
        self._size = None
        self._padding.bind('<Configure>', self._queue_update)

    def _queue_update(self, event_is_ignored):
        """
        Queue update of the board size, but only if it is not already queued.
        """
        if not self._queued:
            self._queued = True
            self._board.after_idle(self._square_it)

    def _square_it(self):
        assert self._queued
        # Allow updates to be queued again
        self._queued = False
        desired = min(self._padding.winfo_width(), self._padding.winfo_height())
        if not self._size == desired:
            # Do updates only if desired size changed
            self._size = desired
            self._board.place(in_=self._padding, x=0, y=0,
                    width=desired, height=desired)

    def get_board_size(self):
        return self._board.winfo_width()

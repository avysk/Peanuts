# coding=utf-8
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
import tkinter as T
from tkinter import messagebox as MB

# noinspection PyPep8
try:
    from tkinter import ttk as TT
    def has_ttk():
        return 'no_ttk' not in sys.argv
except:
    def has_ttk():
        return False

# noinspection PyPep8
try:
    from PIL import Image as I
    from PIL import ImageTk as IT
    def has_pil():
        return 'no_pil' not in sys.argv
except:
    def has_pil():
        return False

from BoardController import BoardController
from UI import UI


def about():
    MB.showinfo("About", "Peanuts v1.0.0.\n(c) 2013, Alexey Vyskubov")


def preferences():
    MB.showerror("Preferences", "Preferences are not implemented.",
                 icon=MB.ERROR)


def main():
    if not has_ttk():
        MB.showerror("No ttk",
                     "No ttk module (Python/Tkinter too old?).\nPeanuts won't run.")
    else:
        controller = BoardController()
        ui = UI(about=about, preferences=preferences, controller=controller,
                app_title='Peanuts',
                min_board_width=400, board_width=500,
                no_pil=('no_pil' in sys.argv))
        controller.open_collection('problems/')
        controller.next_problem()
        if not has_pil():
            MB.showwarning("No PIL", "No PIL library found.")
        ui.run()


if __name__ == '__main__':
    main()

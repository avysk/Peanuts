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
        return not 'no_pil' in sys.argv
except:
    def has_pil():
        return False

from BoardController import BoardController
from UI import UI

def about():
    tkMessageBox.showinfo("About", u"Peanuts v1.0.0.\n© 2013, Alexey Vyskubov")

def preferences():
    tkMessageBox.showerror("Preferences", "Preferences are not implemented.",
            icon=tkMessageBox.ERROR)

def main():
    if not has_ttk():
        tkMessageBox.showerror("No ttk",
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
            tkMessageBox.showwarning("No PIL", "No PIL library found.")
        ui.run()

if __name__ == '__main__':
    main()

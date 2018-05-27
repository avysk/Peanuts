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

import tkinter as tk
from Constants import Color


# pylint: disable=too-many-ancestors
class BoardWidget(tk.Canvas):
    """
    Tkinter widget reperesenting Go board.
    """

    def __init__(self, parent, controller=None, pil=False, **options):
        super(BoardWidget, self).__init__(parent, **options)
        self._controller = controller
        controller.register_board_widget(self)
        self.bind('<Configure>', self.resize)
        self.bind('<Motion>', self.motion)
        self.bind('<Leave>', self.leave)
        self.bind('<Button-1>', self.click)
        self.image = None
        self.texture = None
        if pil:
            from PIL import Image as Im
            from PIL import ImageTk as IT
            self.image = Im.open('images/wood.png')
            self.texture = IT.PhotoImage(self.image)
        self._resize()

    def _resize(self):
        width = self.winfo_width()
        height = self.winfo_height()
        # side
        #   the size of the biggest square which can be fitted into the
        #   canvas.
        # step
        #   1/20 of 'side'. The board lines are one step from each other
        #   and from the square border.
        # _r
        #   the radius of the stone, one half of 'step' minus 1 pixel
        # _points
        #   the array of 21 number, starting from 0 and 'step' from each
        #   other
        self.side = min(width, height)
        self.step = self.side / 20
        self._r = self.step / 2 - 1
        self._points = [self.step * i for i in range(0, 21)]

    def _find_point(self, num):
        """
        Return the closest value to the given number in self._points and its
        index.
        """
        idx = int((num + (self.step / 2)) / self.step)
        # Canvas may be non-square
        if idx > 20:
            idx = 20
        return self._points[idx], idx

    def add_stone(self, nx, ny, color):
        c = {Color.B: 'black', Color.W: 'white'}[color]
        x = self._points[nx + 1]
        y = self._points[ny + 1]
        self.create_oval(x - self._r, y - self._r,
                         x + self._r, y + self._r,
                         fill=c)

    def update_board(self):
        # Clean the board
        self.delete(ALL)
        # Draw the texture
        if self.texture:
            center = self._points[10]
            self.create_image(center, center, image=self.texture)
        # Draw the board border
        start = self._points[1]
        end = self._points[19]
        self.create_polygon(start, start,
                            end, start,
                            end, end,
                            start, end,
                            fill='',
                            outline='black',
                            joinstyle=MITER,
                            width=3)
        # Board lines
        for i in range(17):
            step_i = self.step * (i + 2)
            self.create_line(start, step_i, end, step_i, width=1)
            self.create_line(step_i, start, step_i, end, width=1)
        # Hoshi points
        hr = max(self.step / 10, 2)
        hoshi = [4, 10, 16]
        for ix in hoshi:
            for iy in hoshi:
                x = self._points[ix]
                y = self._points[iy]
                self.create_oval(x - hr, y - hr,
                                 x + hr, y + hr,
                                 fill='black')
        # Stones
        if self._controller:
            for nx, ny, c in self._controller.get_stones():
                self.add_stone(nx, ny, c)
            # Last move
            lm = self._controller.last_move()
            if lm:
                lmx, lmy = lm
                x = self._points[lmx + 1]
                y = self._points[lmy + 1]
                c = {Color.B: '#808080',
                     Color.W: '#A0A0A0'}[self._controller.to_move()]
                o = {Color.B: 'black',
                     Color.W: 'white'}[self._controller.to_move()]
                r = hr * 2
                self.create_oval(x - r, y - r,
                                 x + r, y + r,
                                 fill=c, outline='', width=1)
        # Ko
        self.update_ko()

    def update_ko(self):
        self.delete('ko')
        ko = self._controller.get_ko()
        if ko:
            nxb, nyb = ko
            ko_size = max(self.step/5, 4)
            x = self._points[nxb + 1]
            y = self._points[nyb + 1]
            self.create_polygon(x - ko_size, y - ko_size,
                                x + ko_size, y - ko_size,
                                x + ko_size, y + ko_size,
                                x - ko_size, y + ko_size,
                                fill='',
                                outline='black',
                                joinstyle=MITER,
                                width=1,
                                tag='ko')

    def resize(self, event):
        self._resize()
        self.update_board()

    def motion(self, event):
        self.delete('ghost')
        x, ix = self._find_point(event.x)
        y, iy = self._find_point(event.y)
        nxb = ix - 1
        nyb = iy - 1
        c = {Color.B: '#808080',
             Color.W: '#E0E0E0'}[self._controller.to_move()]
        if ix > 0 and ix < 20 and iy > 0 and iy < 20:
            if self._controller.allowed(nxb, nyb):
                self.create_oval(x - self._r, y - self._r,
                                 x + self._r, y + self._r,
                                 tag='ghost', fill=c)

    def leave(self, event):
        self.delete('ghost')

    def click(self, event):
        x = event.x
        y = event.y
        _, ix = self._find_point(x)
        _, iy = self._find_point(y)
        if ix == 0 or ix == 20 or iy == 0 or iy == 20:
            return
        nxb = ix - 1
        nyb = iy - 1
        if self._controller.allowed(nxb, nyb):
            self.delete('ghost')
            self._controller.add(nxb, nyb)

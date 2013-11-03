from Tkinter import *
from Constants import Color

class BoardWidget(Canvas):

    def __init__(self, parent, controller=None, **options):
        Canvas.__init__(self, parent, **options)
        self._controller = controller
        controller.register_board_widget(self)
        self.bind('<Configure>', self.resize)
        self.bind('<Motion>', self.motion)
        self.bind('<Leave>', self.leave)
        self.bind('<Button-1>', self.click)

    def _resize(self):
        w = self.winfo_width()
        h = self.winfo_height()
        # side
        #   the size of the biggest square which can be fitted into the
        #   canvas.
        # step
        #   1/20 of 'side'. The board lines are one step from each other
        #   and from the square border.
        # r
        #   the radius of the stone, one half of 'step' minus 1 pixel
        # points
        #   the array of 21 number, starting from 0 and 'step' from each
        #   other
        self.side = min(w, h)
        self.step = self.side / 20
        self.r = self.step / 2 - 1
        self.points = [self.step * i for i in xrange(0, 21)]

    def _find_point(self, x):
        """
        Return the closest to x value in self.points and its index.
        """
        ix = (x + (self.step / 2)) / self.step
        # Canvas may be non-square
        if ix > 20: ix = 20
        return self.points[ix], ix

    def add_stone(self, nx, ny, color):
        c = {Color.B: 'black', Color.W: 'white'}[color]
        x = self.points[nx + 1]
        y = self.points[ny + 1]
        self.create_oval(x - self.r, y - self.r, x + self.r, y + self.r,
                fill = c)

    def update(self):
        # Clean the board
        self.delete(ALL)
        # Draw the board border
        start = self.points[1]
        end = self.points[19]
        self.create_polygon(start, start,
                end, start,
                end, end,
                start, end,
                fill='',
                outline='black',
                joinstyle=MITER,
                width=3)
        # Board lines
        for i in xrange(17):
            step_i = self.step * (i + 2)
            self.create_line(start, step_i, end, step_i, width=1)
            self.create_line(step_i, start, step_i, end, width=1)
        # Hoshi points
        hr = max(self.step / 10, 2)
        hoshi = [4, 10, 16]
        for ix in hoshi:
            for iy in hoshi:
                x = self.points[ix]
                y = self.points[iy]
                self.create_oval(x - hr, y - hr, x + hr, y + hr,
                        fill='black')
        # Stones
        if self._controller:
            for nx, ny, c in self._controller.get_stones():
                self.add_stone(nx, ny, c)
            # Last move
            lm = self._controller.last_move()
            if lm:
                lmx, lmy = lm
                x = self.points[lmx + 1]
                y = self.points[lmy + 1]
                c = {Color.B: '#808080',
                     Color.W: '#A0A0A0'}[self._controller.to_move()]
                o = {Color.B: 'black',
                     Color.W: 'white'}[self._controller.to_move()]
                r = hr * 2
                self.create_oval(x - r, y - r, x + r, y + r,
                        fill=c, outline='', width=1)
        # Ko
        self.update_ko()


    def update_ko(self):
        self.delete('ko')
        ko = self._controller.get_ko()
        if ko:
            nxb, nyb = ko
            ko_size = max(self.step/5, 4)
            x = self.points[nxb + 1]
            y = self.points[nyb + 1]
            self.create_polygon(x - ko_size, y - ko_size,
                    x + ko_size, y - ko_size,
                    x + ko_size, y + ko_size,
                    x - ko_size, y + ko_size,
                    fill='',
                    outline='black',
                    joinstyle=MITER,
                    width = 1,
                    tag='ko')

    def resize(self, event):
        self._resize()
        self.update()

    def motion(self, event):
        self.delete('ghost')
        x, ix = self._find_point(event.x)
        y, iy = self._find_point(event.y)
        nxb = ix - 1
        nyb = iy - 1
        c = {Color.B: '#808080',
             Color.W: '#F0F0F0'}[self._controller.to_move()]
        if ix > 0 and ix < 20 and iy > 0 and iy < 20:
            if self._controller.allowed(nxb, nyb):
                self.create_oval(x - self.r, y - self.r, x + self.r, y +
                        self.r, tag='ghost', fill = c)

    def leave(self, event):
        self.delete('ghost')

    def click(self, event):
        x = event.x
        y = event.y
        _, ix = self._find_point(x)
        _, iy = self._find_point(y)
        if ix == 0 or ix == 20 or iy == 0 or iy == 20: return
        nxb = ix - 1
        nyb = iy - 1
        if self._controller.allowed(nxb, nyb):
            self.delete('ghost')
            self._controller.add(nxb, nyb)


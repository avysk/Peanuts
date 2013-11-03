from Constants import Color, Rotation

def _compose(f, g):
    def comp(nx, ny):
        return f(*g(nx, ny))
    return comp

class Transform(object):
    def __init__(self, mirror=False, rotation=Rotation.NONE, swap=False):
        mirror = {False: lambda nx, ny: (nx, ny),
                True: lambda nx, ny: (18 - nx, ny)}[mirror]
        rotate = Rotation.rotate(rotation)
        unrotate = Rotation.unrotate(rotation)
        self.to_board = _compose(rotate, mirror)
        self.from_board = _compose(mirror, unrotate)
        self.fix_color = Color.change_color(swap)

class BoardController(object):
    def __init__(self, model, transform=Transform()):
        self._model = model
        self._to_board = transform.to_board
        self._from_board = transform.from_board
        self._fix_color = transform.fix_color
    def register_board_widget(self, bw):
        self._board_widget = bw
    def get_stones(self):
        stones = self._model.get_stones()
        def stone_to_board((nx, ny, s)):
            nxb, nyb = self._to_board(nx, ny)
            c = self._fix_color(s)
            return (nxb, nyb, c)
        return map(stone_to_board, stones)
    def get_ko(self):
        ko = self._model.get_ko()
        if ko:
            return self._to_board(*ko)
        else:
            return None
    def allowed(self, nxb, nyb):
        nx, ny = self._from_board(nxb, nyb)
        return self._model.allowed(nx, ny)
    def add(self, nxb, nyb):
        nx, ny = self._from_board(nxb, nyb)
        self._model.do_move(nx, ny)
        self._board_widget.update()

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
    def __init__(self, transform=Transform()):
        self._board = [[None for i in xrange(19)] for i in xrange(19)]
        self._ko = None
        self._to_board = transform.to_board
        self._from_board = transform.from_board
        self._fix_color = transform.fix_color
        self._to_move = Color.B
    def register_board_widget(self, bw):
        self._board_widget = bw
    def setup_test_position(self):
        B = Color.B
        W = Color.W
        stones = [(3, 3, B), (2, 2, W), (3, 2, B), (2, 3, W), (2, 4, B),
                (1, 4, W), (2, 5, B), (1, 5, W), (2, 6, B), (3, 1, W),
                (4, 1, B), (2, 1, W), (5, 2, B),
                (1, 2, W), (0, 2, B), (0, 4, B), (0, 3, W)]
        for nx, ny, c in stones:
            self._board[nx][ny] = c
        self._ko = (1, 3)
    def get_stones(self):
        stones = []
        for nx in xrange(19):
            for ny in xrange(19):
                s = self._board[nx][ny]
                if s is not None:
                    nxb, nyb = self._to_board(nx, ny)
                    c = self._fix_color(s)
                    stones.append((nxb, nyb, c))
        return stones
    def get_ko(self):
        if self._ko:
            return self._to_board(*self._ko)
        else:
            return None
    def allowed(self, nxb, nyb):
        nx, ny = self._from_board(nxb, nyb)
        return (self._board[nx][ny] is None) and (self._ko != (nx, ny))
    def add(self, nxb, nyb):
        nx, ny = self._from_board(nxb, nyb)
        self._board[nx][ny] = self._to_move
        # FIXME
        if self._ko:
            self._ko = None
            self._board_widget.update_ko()
        self._board_widget.add_stone(nxb, nyb, self._fix_color(self._to_move))
        self._to_move = Color.change_color(True)(self._to_move)


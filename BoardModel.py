from Constants import Color

_cswap = Color.change_color(True)

class BoardModel(object):
    def __init__(self, size=19):
        self._size = size
        self._board = [[None for i in xrange(size)] for i in xrange(size)]
        self._ko = None
        self._move = Color.B
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
        return [(nx, ny, self._board[nx][ny])
                for nx in xrange(self._size)
                for ny in xrange(self._size)
                if self._board[nx][ny] is not None]
    def get_ko(self):
        return self._ko
    def allowed(self, nx, ny):
        if self._board[nx][ny] is not None:
            return False
        if self._ko == (nx, ny):
            return False
        # FIXME
        return True

    def do_move(self, nx, ny):
        assert(self._board[nx][ny] is None)
        assert(self._ko != (nx, ny))
        self._board[nx][ny] = self._move
        self._move= _cswap(self._move)
        # FIXME
        self._ko = None


    def _has_freedom(self, nx, ny, c):
        f = lambda n, m: not (self._board[n][m] is None)
        return ((nx > 0) and f(nx - 1, ny)) or\
                ((ny > 0) and f(nx, ny -1)) or\
                ((nx < 18) and f(nx + 1, ny)) or\
                ((ny < 18) and f(nx, ny + 1))

    def _get_neighbours(self, nx, ny):
        return [(x, y) for x in [nx - 1, nx, nx + 1]
                for y in [ny - 1, ny, ny + 1]
                if x >= 0 and x < 19 and y >=0 and y < 19 and\
                        (x != nx or y != ny)]
    def _find_killed(self, nx, ny, c):
        killed = [[False for i in xrange(19)] for i in xrange(19)]
        alive = [[False for i in xrange(19)] for i in xrange(19)]
        other = Color.change_color(True)(c)
        nbs = self._get_neighbours(nx, ny)
        for (bx, by) in nbs:
            if self._board[bx][by] != other or\
                    killed[bx][by] or alive[nx][ny]:
                continue
            else:
                self._find_killed_from(bx, by, nx, ny, c, killed, alive)

    def _find_killed_from(sx, sy, ex_x, ex_y, c, killed, alive):
        marked = [[False for i in xrange(19)] for i in xrange(19)]
        marked[sx][sy] = True
        candidates = [(sx, sy)]
        while (len(candidates) > 0):
            cx, cy = candidates.pop()
            ns = self._get_neighbours


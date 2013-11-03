from Constants import Color
import sgflib
import random

_cswap = Color.change_color(True)

class BoardModel(object):
    def __init__(self, size=19):
        self._size = size
        self._board = self._alloc()
        self._ko = None
        self._move_color = Color.B
        self._wrong = False
        self._over = False
        self._cursor = None
        self._lm = None
    def _alloc(self):
        return [[None for i in xrange(self._size)]
                for i in xrange(self._size)]
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
    def to_move(self):
        return self._move_color
    def last_move(self):
        return self._lm
    def allowed(self, nx, ny):
        other_color = _cswap(self._move_color)
        if self._board[nx][ny] is not None:
            return False
        if self._ko == (nx, ny):
            return False
        # Check if we kill something
        killed = self._find_killed(nx, ny, self._move_color)
        we_kill = False
        ns = self._get_neighbours(nx, ny)
        for nx, ny in ns:
            if killed[nx][ny]:
                we_kill = True
                break
        # If we do not kill anything, checki if the move is suicidal
        if not we_kill:
            suicide = True
            self_killed = self._find_killed(nx, ny, other_color)
            for nx, ny in ns:
                if self._board[nx][ny] == other_color:
                    continue
                # If one of neighbours is empty, move is fine
                # If one of neighbours is of move color and won't be
                # killed, move is fine
                if self._board[nx][ny] is None or (not self_killed[nx][ny]):
                    suicide = False
                    break
            if suicide: return False
        return we_kill, killed

    def do_move(self, move_x, move_y, auto=False):
        ok = self.allowed(move_x, move_y)
        assert(ok)
        we_kill, killed = ok

        # Update ko position
        self._ko = self._check_for_ko(move_x, move_y)

        self._board[move_x][move_y] = self._move_color
        self._move_color = _cswap(self._move_color)

        for i in xrange(19):
            for j in xrange(19):
                if killed[i][j]:
                    self._board[i][j] = None
        self._lm = (move_x, move_y)
        if not auto:
            self._check_if_wrong(move_x, move_y)

    def _get_neighbours(self, nx, ny):
        return [(x, y) for (x, y) in
                [(nx - 1, ny), (nx + 1, ny),
                 (nx, ny - 1), (nx, ny + 1)]
                if x >= 0 and x < 19 and y >=0 and y < 19 and\
                        (x != nx or y != ny)]

    def _find_killed(self, move_x, move_y, move_color):
        killed = self._alloc()
        alive = self._alloc()
        other = _cswap(move_color)
        ns = self._get_neighbours(move_x, move_y)
        for nx, ny in ns:
            if self._board[nx][ny] != other or\
                    killed[nx][ny] or alive[nx][ny]:
                continue
            self._find_killed_from((nx, ny), (move_x, move_y),
                    move_color, killed, alive)
        return killed

    def _find_killed_from(self, start, excluded, color, killed, alive):
        start_x, start_y = start
        marked = self._alloc()
        marked[start_x][start_y] = True
        candidates = [start]

        def mark_candidates(cs, to_mark):
            for cx, cy in cs:
                to_mark[cx][cy] = True

        while len(candidates) > 0:
            p = candidates.pop()
            ns = self._get_neighbours(*p)
            for nx, ny in ns:
                # A neighbour of killing color, ignore
                if self._board[nx][ny] == color: continue
                # Empty => all candidates are alive, unless the point is
                # excluded
                if self._board[nx][ny] is None:
                    if (nx, ny) == excluded: continue
                    alive[nx][ny] = True
                    mark_candidates(candidates, alive)
                    return
                else:
                    # A neighbour of our color
                    if alive[nx][ny]:
                        # If it is alive, all candidates are alive
                        mark_candidates(candidates, alive)
                        return
                    elif killed[nx][ny]:
                        # This cannot happen: to have n marked as killed we
                        # had to visit p beforehand
                        assert(False)
                    elif not marked[nx][ny]:
                        # If it is not already marked, it's a candidate
                        marked[nx][ny] = True
                        candidates.append((nx, ny))
        # If we got here, we found no escape route; mark all visited nodes
        # killed
        for i in xrange(self._size):
            for j in xrange(self._size):
                if marked[i][j]:
                    killed[i][j] = True

    def _check_for_ko(self, kx, ky):
        other_color = _cswap(self._move_color)
        assert(self._board[kx][ky] is None)
        # The following conditions have to be satisfied to get ko:
        # (1) (nx, ny) should be surrounded by the stones of other color
        # (2) one and only one of its neighbours should be surrounded by
        # the stones of our color (except in (nx, ny) direction)

        ko = None
        ns = self._get_neighbours(kx, ky)
        for nx, ny in ns: # outer
            # (1)
            if self._board[nx][ny] != other_color: return None
            nns = self._get_neighbours(nx, ny)
            # (2)
            for nnx, nny in nns: # inner
                # exclude ko point
                if nnx == kx and nny == ky:
                    continue # go to inner loop
                # if this one won't be killed, proceed to the next neighbour
                if self._board[nnx][nny] != self._move_color:
                    break # go to outer loop
            else: # inner
                # if we got here, we got ko candidate
                if ko is None:
                    ko = (nx, ny)
                else:
                    # we had another ko candidate before
                    return None
        return ko

    # -----------------------------------------------
    def setup_sgf(self, sgf_string):
        self._ko = None
        self._lm = None
        parser = sgflib.SGFParser(sgf_string)
        collection = parser.parse()
        self._cursor = collection.cursor()
        node = self._cursor.node
        data = node.data
        assert(data['SZ'].data == ['19'])
        assert(data['GM'].data == ['1'])
        assert(data['FF'].data == ['4'])
        if 'HA' in data.keys():
            assert(data['HA'].data == ['0'])
        self._board = self._alloc()
        for b in data['AB']:
            bx = BoardModel._char_to_index(b[0])
            by = BoardModel._char_to_index(b[1])
            self._board[bx][by] = Color.B
        for w in data['AW']:
            wx = BoardModel._char_to_index(w[0])
            wy = BoardModel._char_to_index(w[1])
            self._board[wx][wy] = Color.W
        self._wrong = False
        self._over = False

    @staticmethod
    def _char_to_index(ch):
        assert(len(ch) == 1)
        ch = ch.lower()
        return ord(ch) - ord('a')

    def _check_if_wrong(self, move_x, move_y):
        children = self._cursor.children
        if len(children) == 0:
            print "Got it?", not self._wrong
            return
        for var in xrange(len(children)):
            move = children[var].data['B'].data[0]
            var_x = BoardModel._char_to_index(move[0])
            var_y = BoardModel._char_to_index(move[1])
            if var_x == move_x and var_y == move_y:
                break
        else:
            self._wrong = True
            self._over = True
            print "Wrong and over"
            return
        node = self._cursor.next(var)
        if 'WV' in node.data.keys():
            self._wrong = True
            print "Got into wrong variation."
        children = self._cursor.children
        l = len(children)
        if l == 0:
            print "Got it?", not self._wrong
            return
        var = random.randint(0, l - 1)
        node = self._cursor.next(var)
        reply = node.data['W'].data[0]
        reply_x = BoardModel._char_to_index(reply[0])
        reply_y = BoardModel._char_to_index(reply[1])
        print "reply", reply_x, reply_y
        self.do_move(reply_x, reply_y, auto=True)
        if len(self._cursor.children) == 0:
            self._wrong = True
            print "Refuted."
        else:
            print self._cursor.children[0].data['B'].data




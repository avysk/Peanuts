from Constants import Color
import sgflib
import random

_cswap = Color.change_color(True)

class BoardModel(object):
    def __init__(self, size=19):
        self._size = size
        self._board = self._alloc()
        self._ko = None
        self._last_move = None
        self._move_color = Color.B
        self._wrong = False
        self._over = False
        self._cursor = None

    def _alloc(self):
        return [[None for i in xrange(self._size)]
                for i in xrange(self._size)]

    def setup_position(self, setup):
        self._ko = None
        self._last_move = None
        self._board = self._alloc()
        for color, coords in setup.iteritems():
            for nx, ny in coords:
                self._board[nx][ny] = color

    def get_stones(self):
        return [(nx, ny, self._board[nx][ny])
                for nx in xrange(self._size)
                for ny in xrange(self._size)
                if self._board[nx][ny] is not None]

    def get_ko(self):
        return self._ko

    def to_move(self):
        return self._move_color

    def last_move(self):
        return self._last_move

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

    def do_move(self, move_x, move_y):
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
        self._last_move = (move_x, move_y)

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

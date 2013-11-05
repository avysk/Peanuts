"""
Controller to connect BoardModel with BoardWidget
"""
from Constants import Color, Rotation
from Problem import Problem
from os import listdir
from os.path import isfile, join
import random

def _compose(outer, inner):
    """
    Given an inner function, which takes two arguments and produces 2-tuple,
    and an outer function, which takes two arguments, construct the
    composition of inner function, unpacking, and outer function.
    """
    def comp(arg1, arg2):
        return outer(*inner(arg1, arg2))
    return comp

class Transform(object):
    """
    The class to do different transformations of the board:
    mirroring, rotation and color swap
    """
    def __init__(self, mirror=False, rotation=Rotation.NONE, swap=False):
        mirror = {False: lambda nx, ny: (nx, ny),
                True: lambda nx, ny: (18 - nx, ny)}[mirror]
        rotate = Rotation.rotate(rotation)
        unrotate = Rotation.unrotate(rotation)
        self.to_board = _compose(rotate, mirror)
        self.from_board = _compose(mirror, unrotate)
        self.fix_color = Color.change_color(swap)

class BoardController(object):
    def __init__(self, model, transform=None):
        self._model = model
        if transform is None:
            transform = Transform()
        self._to_board = transform.to_board
        self._from_board = transform.from_board
        self._fix_color = transform.fix_color
        self._board_widget = None
        self._directory = None
        self._collection = None
        self._problem = None

    def register_board_widget(self, widget):
        self._board_widget = widget

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
        self._board_widget.update_board()
        reply = self._problem.get_reply(nx, ny)
        # TODO
        if self._problem.is_over():
            print "Over"
        if self._problem.is_wrong():
            print "Wrong"
        if reply is None:
            print "No reply"
            return
        self._model.do_move(*reply)
        self._board_widget.update_board()

    def to_move(self):
        return self._fix_color(self._model.to_move())

    def last_move(self):
        lm = self._model.last_move()
        if lm:
            lmx, lmy = lm
            return self._to_board(lmx, lmy)
        else:
            return None

    def open_collection(self, directory):
        # FIXME
        self._directory = directory
        self._collection = [f for f in listdir(directory)
                if isfile(join(directory, f))]

    def next_problem(self):
        # FIXME
        l = len(self._collection)
        r = random.randint(0, l - 1)
        f = open(join(self._directory, self._collection[r]))
        self._problem = Problem(f.read())
        self._model.setup_position(self._problem.get_setup())
        self._board_widget.update_board()

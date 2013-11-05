from Constants import Color
import sgflib
import random

class Problem(object):
    def __init__(self, sgf_string):
        # FIXME: exception handling
        parser = sgflib.SGFParser(sgf_string)
        collection = parser.parse()
        self._cursor = collection.cursor()
        node = self._cursor.node
        data = node.data
        # FIXME: support for other board sizes
        assert(data['SZ'].data == ['19'])
        # FIXME: handle failures below
        assert(data['GM'].data == ['1'])
        assert(data['FF'].data == ['4'])
        if 'HA' in data.keys():
            assert(data['HA'].data == ['0'])
        self._setup = {}
        self._setup[Color.B] =\
                [(Problem._char_to_index(b[0]), Problem._char_to_index(b[1]))
                        for b in data['AB']]
        self._setup[Color.W] =\
                [(Problem._char_to_index(w[0]), Problem._char_to_index(w[1]))
                        for w in data['AW']]
        self._wrong = False
        self._over = False

    def get_setup(self):
        return self._setup

    def is_over(self):
        return self._over

    def is_wrong(self):
        return self._wrong

    def get_reply(self, move_x, move_y):
        self._check_if_wrong(move_x, move_y)
        return self._reply

    @staticmethod
    def _char_to_index(ch):
        assert(len(ch) == 1)
        # FIXME: handle bad results
        return ord(ch) - ord('a')

    def _check_if_wrong(self, move_x, move_y):
        self._reply = None
        children = self._cursor.children
        if len(children) < 0:
            self._over = true
            return
        # var stands for "variation"
        for var in xrange(len(children)):
            move = children[var].data['B'].data[0]
            var_x = Problem._char_to_index(move[0])
            var_y = Problem._char_to_index(move[1])
            if (var_x, var_y) == (move_x, move_y):
                break
        else: # variation is not found
            self._wrong = True
            self._over = True
            return
        node = self._cursor.next(var)
        # TODO: other Uligo and GoGrinder compatible ways to detect the wrong
        # variation
        # TODO: variation marked as wrong only in the last move of the variation
        if 'WV' in node.data.keys():
            self._wrong = True
        children = self._cursor.children
        replies = len(children)
        if replies == 0:
            self._over = True
            return
        var = random.randint(0, replies - 1)
        node = self._cursor.next(var)
        reply = node.data['W'].data[0]
        reply_x = Problem._char_to_index(reply[0])
        reply_y = Problem._char_to_index(reply[1])
        if len(self._cursor.children) == 0:
            self._wrong = True
            self._over = True
        self._reply = (reply_x, reply_y)

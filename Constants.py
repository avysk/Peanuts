class Color(object):
    B = 0
    W = 1

    @staticmethod
    def change_color(swap):
        return {False: lambda c: c,
                True: lambda c: 1 - c}[swap]


class Rotation(object):
    NONE = 0
    RIGHT = 1
    LEFT = 2
    BOTH = 3

    @staticmethod
    def rotate(rotation):
        return {Rotation.NONE: lambda n, m: (n, m),
                Rotation.RIGHT: lambda n, m: (18 - m, n),
                Rotation.LEFT: lambda n, m: (m, 18 - n),
                Rotation.BOTH: lambda n, m: (18 - n, 18 - m)}[rotation]

    @staticmethod
    def unrotate(rotation):
        return {Rotation.NONE: lambda n, m: (n, m),
                Rotation.RIGHT: lambda n, m: (m, 18 - n),
                Rotation.LEFT: lambda n, m: (18 - m, n),
                Rotation.BOTH: lambda n, m: (18 - n, 18 - m)}[rotation]


# coding=utf-8
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

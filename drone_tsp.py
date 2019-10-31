from tkinter import *

from area import DefCoord
from tsp import FindRoot


class DefineArea:
    """ Определение прямоугольника, в котором надо произвести съемку """

    def __init__(self, base, ul, br, side):
        self.base = base
        self.top_left = ul
        self.bottom_right = br
        self.side = side
        self.new_route = None
        self.set_area()

    def set_area(self):

        # Получить массив координат для съемки
        area = DefCoord((self.top_left[0], self.top_left[1],
                         self.bottom_right[0], self.bottom_right[1]), self.side)
        coord = area.get_area()
        print("Points: ", coord)
        coord.insert(0, self.base)

        r = FindRoot(coord)  # Решение задачи комивояжера
        self.new_route = r.get_root()
        print("Route: ", self.new_route)

    def get_route(self):
        return self.new_route


def main(args_list: list):

    base, side = (args_list[0], args_list[1]), args_list[6]
    rect = [args_list[2], args_list[3], args_list[4], args_list[5]]

    ul = (min(rect[0], rect[2]), max(rect[1], rect[3]))
    br = (max(rect[0], rect[2]), min(rect[1], rect[3]))

    print("BASE={}, UL={}, BR={}, Side={}".format(base, ul, br, side))

    da = DefineArea(base, ul, br, side)  # Определить область съемки
    return da.get_route()  # tsp route


if __name__ == '__main__':
    if len(sys.argv) == 8:
        try:
            ll = list(map(float, sys.argv[1:]))
        except:
            print('Incorrect numbers', sys.argv[1:])
            sys.exit(1)
    else:
        print("Number of input parameters must be 6: Base(x1,y1), Rect(x2,y2,x3,y3), Side(n)", sys.argv[1:])
        sys.exit(1)

    if ll[6] > 0:
        main(ll)
    else:
        print("Check if Side > 0: ", ll[6])

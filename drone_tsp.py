from tkinter import *

from area import DefCoord
from tsp import FindRoot


class DefineArea:
    """ Определение прямоугольника, в котором надо произвести съемку """

    def __init__(self, base, ul, br):
        self.base = base
        self.top_left = ul
        self.bottom_right = br
        self.new_route = None
        self.set_area()

    def set_area(self):

        # Получить массив координат для съемки
        area = DefCoord((self.top_left[0], self.top_left[1],
                         self.bottom_right[0], self.bottom_right[1]))
        coord = area.get_area()
        print("Points: ", coord)
        coord.insert(0, self.base)

        r = FindRoot(coord)  # Решение задачи комивояжера
        self.new_route = r.get_root()
        print("Route: ", self.new_route)

    def get_route(self):
        return self.new_route


def main(args_list: list):

    base, ul, br = (args_list[0], args_list[1]), (args_list[2], args_list[3]), (args_list[4], args_list[5])
    print("BASE={}, UL={}, BR={}".format(base, ul, br))

    da = DefineArea(base, ul, br)  # Определить область съемки

    return da.get_route()  # tsp route


if __name__ == '__main__':
    if len(sys.argv) == 7:
        try:
            ll = list(map(int, sys.argv[1:]))
        except:
            print('Incorrect integers', sys.argv[1:])
            sys.exit(1)
    else:
        print("Number of input parameters must be 6: Base(x,y), UL(x,y), BR(x,y)", sys.argv[1:])
        sys.exit(1)

    if all(item >= 0 for item in ll) and (ll[2] < ll[4]) and (ll[3] < ll[5]):
        main(ll)
    else:
        print("Check if >= 0 and UpperLeft < BottomRight", ll)

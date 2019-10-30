from tkinter import *

from area import DefCoord
from tsp import FindRoot


class Drone:
    """ Физическая модель дрона """

    def __init__(self):
        self.full_charge = 600  # Полный заряд дрона
        self.delta_e_flying = 1  # Расход энергии на единицу пройденного расстояния
        self.delta_e_shooting = 4  # Расход энергии на рдин снимок

    # Возвращает расстояние между точками
    @staticmethod
    def distance(l: tuple) -> float:
        return (abs(l[2] - l[0]) ** 2 + abs(l[3] - l[1]) ** 2) ** 0.5

    # Возвращает радиус круга
    def max_radius(self) -> float:
        max_distance = (self.full_charge - self.delta_e_shooting) / self.delta_e_flying
        return max_distance / 2

    def get_full_charge(self):
        return self.full_charge

    def set_full_charge(self, new_value):
        self.full_charge -= new_value
        return


class DefineArea:
    """ Определение прямоугольника, в котором надо произвести съемку """

    def __init__(self, key_adapter, base, ul, br):
        self.ka = key_adapter
        self.base = base
        self.top_left = ul
        self.bottom_right = br
        self.new_route = None
        self.set_area()

    def set_area(self):
        self.ka.canvas.create_rectangle(self.top_left[0], self.top_left[1],
                                        self.bottom_right[0], self.bottom_right[1], dash=(4, 2))

        # Получить массив координат для съемки
        area = DefCoord((self.top_left[0], self.top_left[1],
                         self.bottom_right[0], self.bottom_right[1]))
        coord = area.get_area()
        coord.insert(0, self.base)

        r = FindRoot(coord)  # Решение задачи комивояжера
        self.new_route = r.get_root()
        print("Route: ", self.new_route)

        obj = CalcRoot(self.ka, coord, self.new_route)
        obj.view_points()
        obj.drawing_root()

    def get_route(self):
        return self.new_route


class CalcRoot:
    """ Отображение маршрута после решения задачи комивояжера """

    def __init__(self, key_adapter, coord: list, new_root: list):
        self.ka = key_adapter
        self.coord = coord
        self.root = new_root

    def drawing_point(self, x, y, radius=2, color="blue"):
        self.ka.canvas.create_oval(x - radius, y + radius, x + radius, y - radius, fill=color)

    def drawing_line(self, x1, y1, x2, y2, color):
        self.ka.canvas.create_line(x1, y1, x2, y2, dash=(4, 2), arrow=LAST, fill=color)

    def view_points(self):
        for point in self.coord:
            self.drawing_point(point[0], point[1], 3, "blue")

    def drawing_root(self):
        total = 0

        for i in range(len(self.root)):
            x1 = self.root[i][0]
            y1 = self.root[i][1]

            if i == len(self.root) - 1:
                x2 = self.root[0][0]
                y2 = self.root[0][1]
            else:
                x2 = self.root[i + 1][0]
                y2 = self.root[i + 1][1]

            self.drawing_line(x1, y1, x2, y2, "blue")
            total += Drone.distance((x1, y1, x2, y2))
        print("Total distance: {:7.2f}".format(total))


class KeyAdapter:
    """ Связывает события и кнопки """

    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.canvas.bind('<Button-2>', self.exit_app)

    # Выход из программы - правая кнопка мыши
    @staticmethod
    def exit_app(self):
        sys.exit()


def main(args_list: list):
    base, ul, br = (args_list[0], args_list[1]), (args_list[2], args_list[3]), (args_list[4], args_list[5])
    print("BASE={}, UL={}, BR={}".format(base, ul, br))
    root = Tk()
    root.title("Area Shooting")

    can = Canvas(root, width=1400, height=820, bg="lightgreen")
    can.pack(fill='both', expand=True)

    ka = KeyAdapter(root, can)  # Определить выход из программы по правой клавише мышки
    my_drone = Drone()
    da = DefineArea(ka, base, ul, br)  # Определить область съемки

    root.mainloop()
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

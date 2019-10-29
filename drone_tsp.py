from tkinter import *

import const
from area import DefCoord
from tsp import FindRoot


class Drone:
    """ Физическая модель дрона """

    def __init__(self):
        self.full_charge = 600  # Полный заряд дрона
        self.delta_e_flying = 1  # Расход энергии на единицу пройденного расстояния
        self.delta_e_shooting = 4  # Расход энергии на рдин снимок

    # l - кортеж, координаты начальной точки (x1, y1) и конечной точки (x2, y2)
    # l = (x1, y1, x2, y2)
    # Возвращает расстояние между точками
    @staticmethod
    def distance(l: tuple) -> float:
        return (abs(l[2] - l[0]) ** 2 + abs(l[3] - l[1]) ** 2) ** 0.5

    # Максимальное расстояние полета (туда и обратно) + один снимок
    # Зависит от начальной энергии и расхода на единицу полета и снимок
    # Возвращает радиус круга
    def max_radius(self) -> float:
        max_distance = (self.full_charge - self.delta_e_shooting) / self.delta_e_flying
        return max_distance / 2

    def get_full_charge(self):
        return self.full_charge

    def set_full_charge(self, new_value):
        self.full_charge -= new_value
        print("Остаток энергии: {:5.2f}".format(self.get_full_charge()))
        return


class DefineArea:
    """ Определение прямоугольника, в котором надо произвести съемку """

    def __init__(self, key_adapter):
        self.ka = key_adapter
        self.top_left = ()
        self.bottom_right = ()
        self.ka.add_button1(self.set_area)

    def set_area(self, event):
        point = (int(event.x), int(event.y))
        if not self.top_left:
            self.top_left = point
            self.ka.canvas.create_oval(point[0] - 2, point[1] + 2, point[0] + 2, point[1] - 2,
                                       fill="blue")
        elif point[0] > self.top_left[0] and point[1] > self.top_left[1]:
            self.bottom_right = point

            self.ka.del_button1()
            self.ka.canvas.create_rectangle(self.top_left[0], self.top_left[1],
                                            self.bottom_right[0], self.bottom_right[1], dash=(4, 2))

            # Получить массив координат для съемки
            area = DefCoord((self.top_left[0], self.top_left[1],
                             self.bottom_right[0], self.bottom_right[1]))
            coord = area.get_area()
            coord.append(const.BASE)

            r = FindRoot(coord)  # Решение задачи комивояжера
            new_root = r.get_root()

            obj = CalcRoot(self.ka, coord, new_root)
            obj.view_points()
            obj.drawing_root()


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

        # База дрона
        self.drawing_point(const.BASE[0], const.BASE[1], 5, "darkred")

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

    def add_button1(self, func):
        self.canvas.bind('<Button-1>', func)

    def del_button1(self):
        self.canvas.unbind('<Button-1>')

    # Выход из программы - правая кнопка мыши
    @staticmethod
    def exit_app(self):
        sys.exit()


def main():
    root = Tk()
    root.title("Area Shooting")

    can = Canvas(root, width=1400, height=820, bg="lightgreen")
    can.pack(fill='both', expand=True)

    ka = KeyAdapter(root, can)
    my_drone = Drone()

    # Определить область съемки
    da = DefineArea(ka)

    root.mainloop()


if __name__ == '__main__':
    main()

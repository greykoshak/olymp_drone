# Шаг для съемки
SIDE = 50


class DefCoord:
    """ Определение массива точек аэрофотосъемки """

    def __init__(self, coord: tuple):
        self.points = list()
        self.xp1 = coord[0]
        self.yp1 = coord[1]
        self.xp2 = coord[2]
        self.yp2 = coord[3]

        # main, assign/calculate
        len_x = self.xp2 - self.xp1
        len_y = self.yp2 - self.yp1

        if len_x % SIDE == 0:
            num_x = len_x // SIDE
        else:
            num_x = len_x // SIDE + 1

        if len_y % SIDE == 0:
            num_y = len_y // SIDE
        else:
            num_y = len_y // SIDE + 1

        # main, fill
        for i in range(int(num_x)):
            for j in range(int(num_y)):
                self.points.append((min(self.xp1, self.xp2) + SIDE / 2 + SIDE * i,
                                    min(self.yp1, self.yp2) + SIDE / 2 + SIDE * j))

    def get_area(self):
        return self.points

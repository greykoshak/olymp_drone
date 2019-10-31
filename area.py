class DefCoord:
    """ Определение массива точек аэрофотосъемки """

    def __init__(self, coord: tuple, side):
        self.points = list()
        self.xp1 = coord[0]
        self.yp1 = coord[1]
        self.xp2 = coord[2]
        self.yp2 = coord[3]
        self.side = side

        # main, assign/calculate
        len_x = self.xp2 - self.xp1
        len_y = self.yp2 - self.yp1

        if len_x % self.side == 0:
            num_x = len_x // self.side
        else:
            num_x = len_x // self.side + 1

        if len_y % self.side == 0:
            num_y = len_y // self.side
        else:
            num_y = len_y // self.side + 1

        # main, fill
        for i in range(int(num_x)):
            for j in range(int(num_y)):
                self.points.append((min(self.xp1, self.xp2) + self.side / 2 + self.side * i,
                                    min(self.yp1, self.yp2) + self.side / 2 + self.side * j))

    def get_area(self):
        return self.points

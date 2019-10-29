import numpy as np
from numpy import sqrt


class FindRoot:
    def __init__(self, coord):
        self.coord = coord
        self.out = list()

    def computing(self):
        X = [k[0] for k in self.coord]
        Y = [k[1] for k in self.coord]

        n = len(X)
        RS, RW, RIB, s = list(), list(), list(), list();

        for ib in np.arange(0, n, 1):
            M = np.zeros([n, n])
            for i in np.arange(0, n, 1):
                for j in np.arange(0, n, 1):
                    if i != j:
                        M[i, j] = sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
                    else:
                        M[i, j] = float('inf')

            way = list()
            way.append(ib)

            for i in np.arange(1, n, 1):
                s = list()
                for j in np.arange(0, n, 1):
                    s.append(M[way[i - 1], j])
                way.append(s.index(min(s)))
                for j in np.arange(0, i, 1):
                    M[way[i], way[j]] = float('inf')
                    M[way[i], way[j]] = float('inf')
            S = sum([sqrt((X[way[i]] - X[way[i + 1]]) ** 2 + (Y[way[i]] - Y[way[i + 1]]) ** 2)
                     for i in np.arange(0, n - 1, 1)]) + sqrt((X[way[n - 1]] - X[way[0]]) ** 2 +
                                                              (Y[way[n - 1]] - Y[way[0]]) ** 2)
            RS.append(S)
            RW.append(way)
            RIB.append(ib)

        S = min(RS)
        way = RW[RS.index(min(RS))]
        ib = RIB[RS.index(min(RS))]

        X1 = [X[way[i]] for i in np.arange(0, n, 1)]
        Y1 = [Y[way[i]] for i in np.arange(0, n, 1)]

        self.out = [tuple(tup) for tup in zip(X1, Y1)]

    def get_root(self):
        self.computing()
        return self.out

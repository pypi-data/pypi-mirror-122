import numpy as np

#   https://www.ams.org/journals/mcom/1970-24-109/S0025-5718-1970-0258240-X/S0025-5718-1970-0258240-X.pdf

class MyKroghInterpolator:

    def __init__(self, xi, yi):
        self.xi = xi
        self.yi = yi
        self.n = len(self.xi)

        c = np.zeros(self.n + 1)
        c[0] = self.yi[0]

        V = np.zeros((self.n, self.n))

        for k in range(1, self.n):
            s = 0
            while s <= k and xi[k - s] == xi[k]:
                s += 1

            s -= 1
            V[0][k] = self.yi[k]

            for i in range(k - s):
                if s == 0:
                    V[i + 1][k] = (c[i] - V[i][k]) / (xi[i] - xi[k])
                else:
                    V[i + 1][k] = (V[i + 1][k - 1] - V[i][k]) / (xi[i] - xi[k])

            c[k] = V[k - s][k]
        self.c = c

    def __call__(self, x):
        pi = np.zeros((self.n, len(x)))
        pi[0] += 1

        p = np.zeros((self.n, len(x)))
        p[0] += self.c[0]

        w = np.zeros((self.n, len(x)))

        for k in range(1, self.n):
            w[k - 1] = x - self.xi[k - 1]
            pi[k] = w[k - 1] * pi[k - 1]
            p[k] = p[k - 1] + pi[k] * self.c[k]

        return p[-1]

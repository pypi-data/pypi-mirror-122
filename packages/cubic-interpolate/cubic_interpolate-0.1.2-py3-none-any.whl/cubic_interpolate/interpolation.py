import numpy as np
import matplotlib.pyplot as plt

def c_interp(x, y):
    xnew = np.arange(min(x), max(x), 0.01)
    plt.rcParams['figure.figsize'] = (12, 5)
    size = len(x)

    h = []
    F = []
    X = np.zeros(shape=(size, size))

    for i in range(size - 1):
        hh = x[i + 1] - x[i]
        h.append(hh)

    F.append(0)
    for i in range(1, size - 1):
        ff = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])
        F.append(ff)
    F.append(0)

    X[0][0] = 1
    X[size - 1][size - 1] = 1
    for i in range(1, size - 1):
        X[i][i - 1] = h[i - 1]
        X[i][i] = (h[i - 1] + h[i]) * 2
        X[i][i + 1] = h[i]

    C = np.linalg.solve(X, F)
    C[0] = 0
    C[size - 1] = 0

    A = []
    B = []
    D = []
    for i in range(size - 1):
        a = y[i]
        b = (y[i + 1] - y[i]) / h[i] - h[i] * (2 * C[i] + C[i + 1]) / 3
        d = (C[i + 1] - C[i]) / (3 * h[i])
        A.append(a)
        B.append(b)
        D.append(d)

    for i in range(size - 1):
        x_new = np.arange(x[i], x[i + 1], 0.005)
        dif = x_new - x[i]
        yy = A[i] + B[i] * dif + C[i] * (dif ** 2) + D[i] * (dif ** 3)
        plt.plot(x_new, yy, 'b')

    # plt.plot(xnew, y1, 'g', label='linear')
    # plt.plot(xnew, y2, 'r', label='cubic')
    # plt.plot([], [], color='b', label='My function')
    plt.scatter(x, y)
    plt.show()

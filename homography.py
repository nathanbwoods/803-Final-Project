import numpy as np
from scipy.optimize import minimize

class Transformer:

    def __init__(self, H=None, img_size=512):
        self.H = H
        self.image_size = img_size

    def homography_transform(self, X):
        n = X.shape[0]
        r = X[:, 3]

        # select x, y, z, add homogeneous coordinate
        X = X[:, 0:3]
        X = np.hstack([X, np.ones((n, 1))])

        # Compute u, v, s
        Y = X.dot(self.H.T)

        # Normalize
        Yn = Y[:, 0:2] / Y[:, 2:3]

        # Create offset points corresponding to the radius of each unit
        Xd = X + np.vstack([r, r, np.zeros(n), np.zeros(n)]).T

        # Compute u, v for the offset points
        Yd = Xd.dot(self.H.T)
        Ydn = Yd[:, 0:2] / Yd[:, 2:3]

        # Find the shift from Yn to Ydn, x and y shifts correspond to the width and height of the bouding box
        dn = np.abs(Ydn - Yn)
        wh = dn * 2

        return np.hstack((Yn, wh))

    def fit_homography(self, x, y):
        # Scale to (0, 1)
        y /= self.image_size
        n = x.shape[0]

        # Set up homogeneous system of linear equations
        A = np.zeros([2*n, 12])
        for i in range(n):
            u = y[i][0]
            v = y[i][1]
            X = x[i][0]
            Y = x[i][1]
            Z = x[i][2]

            A[i*2] = [-X,-Y,-Z,-1,0,0,0,0, X*u, Y*u, Z*u, 1]
            A[i*2 + 1] = [0,0,0,0,-X,-Y,-Z,-1,X*v,Y*v, Z*v, 1]

        # Find initial solution
        w, v = np.linalg.eig(np.dot(A.T, A))
        h = v[:, np.argmin(w)]

        h = np.ascontiguousarray(h)

        # Use initial solution as input for non-linear optimization
        homography_minimizer = HomographyMinimizer(x, y)
        cons = ({'type':'eq', 'fun': lambda x: x[11] - 1})
        res = minimize(homography_minimizer.homography_diff, h, constraints=cons, method='SLSQP')

        h = res.x

        self.H = np.reshape(h, (3, 4))


class HomographyMinimizer:

    def __init__(self, X, y):
        n = X.shape[0]
        self.X = np.hstack([X, np.ones((n, 1))])
        self.y = y

    def homography_diff(self, H):
        H = np.vstack([H[0:4], H[4:8], H[8:]])

        Y = H.dot(self.X.T).T
        Yn = Y[:, 0:2] / Y[:, 2:3] # Y, normalized
        return np.sum(np.power(self.y - Yn, 2))


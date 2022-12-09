import numpy as np
from scipy.optimize import minimize

class Transformer:

    def __init__(self, H=None, x_scale=None, y_scale=None, img_size=512):
        self.H = H
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.image_size = img_size

    def homography_transform(self, X):
        n = X.shape[0]

        X = np.hstack([X, np.ones((n, 1))])

        Y = self.H.dot(X.T).T
        Yn = Y[:, 0:2] / Y[:, 2:3] # Y, normalized
        return Yn

    def fit_homography(self, x, y):
        y /= self.image_size
        n = x.shape[0]

        # A = np.zeros([2*n, 11])
        # for i in range(n):
        #     u = y[i][0]
        #     v = y[i][1]
        #     X = x[i][0]
        #     Y = x[i][1]
        #     Z = x[i][2]
        #
        #     A[i*2] = [X,Y,Z,1,0,0,0,0, -X*u, -Y*u, -Z*u]
        #     A[i*2 + 1] = [0,0,0,0,X,Y,Z,1,-X*v,-Y*v, -Z*v]
        #
        # h = np.linalg.lstsq(A, y.flatten(), rcond=None)[0]
        #
        # h = np.append(h, 1)

        A = np.zeros([2*n, 12])
        for i in range(n):
            u = y[i][0]
            v = y[i][1]
            X = x[i][0]
            Y = x[i][1]
            Z = x[i][2]

            A[i*2] = [-X,-Y,-Z,-1,0,0,0,0, X*u, Y*u, Z*u, 1]
            A[i*2 + 1] = [0,0,0,0,-X,-Y,-Z,-1,X*v,Y*v, Z*v, 1]

        w, v = np.linalg.eig(np.dot(A.T, A))
        h = v[:, np.argmin(w)]

        h = np.ascontiguousarray(h)

        homography_minimizer = HomographyMinimizer(x, y)
        cons = ({'type':'eq', 'fun': lambda x: x[11] - 1})

        res = minimize(homography_minimizer.homography_diff, h, constraints=cons, method='SLSQP')

        print(res.message)

        h = res.x

        self.H = np.reshape(h, (3, 4))




        # TODO: Perform this per unit instead of per frame,
        # and add a Z-scale calculation.
        # scale_points = np.array([[0, 0, 12], [0, 1, 12], [1, 0, 12]])
        # scale = self.homography_transform(scale_points)
        # print(scale)
        # self.x_scale = np.linalg.norm(scale[0] - scale[1])
        # self.y_scale = np.linalg.norm(scale[0] - scale[2])
        self.x_scale = 0.05
        self.y_scale = 0.05

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


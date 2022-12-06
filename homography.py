import numpy as np


class Transformer:

    def __init__(self, H=None, x_scale=None, y_scale=None, img_size=1024):
        self.H = H
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.image_size = img_size

    def homography_transform(self, X):
        n = X.shape[0]
        X = np.hstack([X, np.ones((n, 1))])
        Y = np.array([np.matmul(self.H, X[i]) for i in range(n)])
        Y = Y[:, 0:2] / Y[:, 2:3]
        return Y

    def fit_homography(self, x, y):
        y /= self.image_size
        n = x.shape[0]
        A = np.zeros([2*n, 11])
        for i in range(n):
            v = y[i][0]
            u = y[i][1]
            X = x[i][0]
            Y = x[i][1]
            Z = x[i][2]

            A[i*2] = [X,Y,Z,1,0,0,0,0, -X*u, -Y*u, -Z*u]
            A[i*2 + 1] = [0,0,0,0,X,Y,Z,1,-X*v,-Y*v, -Z*v]

        x = np.linalg.lstsq(A, y.flatten(), rcond=None)[0]
        h = np.append(x, [1])

        self.H = np.vstack([h[0:4], h[4:8], h[8:]])

        scale_points = np.array([[0, 0, 12], [0, 1, 12], [1, 0, 12]])
        scale = self.homography_transform(scale_points)

        self.x_scale = np.linalg.norm(scale[0] - scale[1]) * 2
        self.y_scale = np.linalg.norm(scale[0] - scale[2]) * 2


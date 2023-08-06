import numpy as np
from boss.utils.arrays import shape_consistent_XY


class UserFunc:
    """Wrapper class for BOSS user functions. """

    def __init__(self, func, dim):
        self.func = func
        self.dim = dim

    def eval(self, X_in, ygrad=False):
        X_in = np.atleast_2d(X_in)
        output = self.func(X_in)

        if isinstance(output, tuple):
            if not ygrad:
                X_out = output[0]
                Y = output[1]
            else:
                if len(output) > 2:
                    X_out = output[0]
                    Y = np.atleast_2d(output[1])
                    dY = np.atleast_2d(output[2])
                else:
                    X_out = X_in
                    Y = np.atleast_2d(output[0])
                    dY = np.atleast_2d(output[1])
                Y = np.concatenate((Y, dY), axis=1)
        else:
            Y = output
            X_out = X_in

        return shape_consistent_XY(X_out, Y, self.dim, ygrad=ygrad)

    def __call__(self, X_in):
        return self.eval(X_in)

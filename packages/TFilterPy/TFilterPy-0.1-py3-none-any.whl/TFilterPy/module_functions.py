import numpy as np
from numpy.linalg import inv

class KalmanFilter:
    r"""
    A short description of your class.

    Parameters
    ----------
    arg1 : int
        Description of arg1.
    arg2 : numpy.ndarray
        Description of arg2.
    """
    def __init__(self, F, H, Q, R, x0, P0):
        self.F = F  # state transition matrix
        self.H = H  # observation matrix
        self.Q = Q  # process noise covariance matrix
        self.R = R  # observation noise covariance matrix
        self.x = x0  # initial state estimate
        self.P = P0  # initial state covariance estimate
        
    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        
    def update(self, z):
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(self.P.shape[0]) - K @ self.H) @ self.P
        
    def run(self, measurements):
        self.x = np.array(self.x)
        self.P = np.array(self.P)
        
        state_estimates = []
        for z in measurements:
            self.predict()
            self.update(z)
            state_estimates.append(self.x)
        return state_estimates
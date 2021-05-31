import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Koker:

    def __init__(self):
        self.x = None
        self.x_train = None
        self.x_test = None
        self.theta = None
        self.sharpes = None

    def load(self, data):
        """
        Load a dataframe with the data and create the training and test set.
        The column with the timestamp must be labelled 'utc' and the one with
        price, "price".

        :param data: DataFrame
        """
        data.index = pd.to_datetime(data.index, unit='s')
        rets = data['price'].diff()[1:]

        x = np.array(rets)
        self.x = x

        N = 1000
        P = 200
        x_train = x[-(N+P):-P]
        x_test = x[-P:]

        std = np.std(x_train)
        mean = np.mean(x_train)

        self.x_train = (x_train - mean) / std
        self.x_test = (x_test - mean) / std

    @staticmethod
    def sharpe_ratio(rets):
        return rets.mean() / rets.std()

    @staticmethod
    def positions(x, theta):
        M = len(theta) - 2
        T = len(x)
        Ft = np.zeros(T)
        for t in range(M, T):
            xt = np.concatenate([[1], x[t - M:t], [Ft[t - 1]]])
            Ft[t] = np.tanh(np.dot(theta, xt))
        return Ft

    @staticmethod
    def returns(Ft, x, delta):
        T = len(x)
        rets = Ft[0:T - 1] * x[1:T] - delta * np.abs(Ft[1:T] - Ft[0:T - 1])
        return np.concatenate([[0], rets])

    @staticmethod
    def gradient(x, theta, delta):
        Ft = Koker.positions(x, theta)
        R = Koker.returns(Ft, x, delta)
        T = len(x)
        M = len(theta) - 2

        A = np.mean(R)
        B = np.mean(np.square(R))
        S = A / np.sqrt(B - A ** 2)

        dSdA = S * (1 + S ** 2) / A
        dSdB = -S ** 3 / 2 / A ** 2
        dAdR = 1. / T
        dBdR = 2. / T * R

        grad = np.zeros(M + 2)  # initialize gradient
        dFpdtheta = np.zeros(M + 2)  # for storing previous dFdtheta

        for t in range(M, T):
            xt = np.concatenate([[1], x[t - M:t], [Ft[t - 1]]])
            dRdF = -delta * np.sign(Ft[t] - Ft[t - 1])
            dRdFp = x[t] + delta * np.sign(Ft[t] - Ft[t - 1])
            dFdtheta = (1 - Ft[t] ** 2) * (xt + theta[-1] * dFpdtheta)
            dSdtheta = (dSdA * dAdR + dSdB * dBdR[t]) * (
                        dRdF * dFdtheta + dRdFp * dFpdtheta)
            grad = grad + dSdtheta
            dFpdtheta = dFdtheta

        return grad, S

    def train(self, x, epochs=2000, M=8, commission=0.0025, learning_rate=0.3):
        print("training : start")
        theta = np.random.rand(M + 2)
        sharpes = np.zeros(epochs)  # store sharpes over time
        for i in range(epochs):
            grad, sharpe = Koker.gradient(x, theta, commission)
            theta = theta + grad * learning_rate
            sharpes[i] = sharpe
        self.theta = theta
        self.sharpes = sharpes
        print("training : completed")

    def plot(self, x, theta):
        x_returns = Koker.returns(Koker.positions(x, theta), x, 0.0025)
        plt.plot(x_returns.cumsum(), label="Reinforcement Learning Model", linewidth=1)
        plt.plot(x.cumsum(), label="Buy and Hold", linewidth=1)
        plt.xlabel('Ticks')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.title("RL Model vs. Buy and Hold")

#read train data
import sys

class Simple_Kalman:

    def __init__(self, observation, start_position, start_deviation, deviation_true, deviation_noise):

        self.obs = observation
        self.n_obs = len(observation)
        self.start_pos = start_position
        self.start_dev = start_deviation
        self.dev_q = deviation_true
        self.dev_r = deviation_noise

        self._fit()

    def _forward(self):

        self.x_prev_ = [self.start_pos]
        self.P_prev_ = [self.start_dev]
        self.K_ = [self.P_prev_[0] / (self.P_prev_[0] + self.dev_r)]
        self.P_ = [self.dev_r * self.P_prev_[0] / (self.P_prev_[0] + self.dev_r)]
        self.x_ = [self.x_prev_[0] + self.K_[0] * (self.obs[0] - self.x_prev_[0])]

        for t in range(1, self.n_obs):
            self.x_prev_.append(self.x_[t - 1])
            self.P_prev_.append(self.P_[t - 1] + self.dev_q)

            self.K_.append(self.P_prev_[t] / (self.P_prev_[t] + self.dev_r))
            self.x_.append(self.x_prev_[t] + self.K_[t] * (self.obs[t] - self.x_prev_[t]))
            self.P_.append(self.dev_r * self.P_prev_[t] / (self.P_prev_[t] + self.dev_r))

    def _backward(self):

        self.x_all_ = [self.x_[-1]]
        self.P_all_ = [self.P_[-1]]
        self.C_ = [self.P_[-1] / (self.P_[-1] + self.dev_q)]

        for t in range(2, self.n_obs + 1):
            self.C_.append(self.P_[-t] / (self.P_[-t] + self.dev_q))
            self.x_all_.append(self.x_[-t] + self.C_[-1] * (self.x_all_[-1] - self.x_prev_[-t + 1]))
            self.P_all_.append(self.P_[-t] + (self.C_[-1] ** 2) * (self.P_all_[-1] - self.P_prev_[-t + 1]))

        self.C_.reverse()
        self.x_all_.reverse()
        self.P_all_.reverse()

    def _fit(self):
        self._forward()
        self._backward()



if __name__ == "__main__":
    print(sys.path)
    print('==>Kalman Filter imported')
import numpy as np
import cfg


class Tank:
    standard_size = 20

    def __init__(self, n_tanks, init_storage, roof):
        self.n_tanks = n_tanks
        self.init_storage = init_storage
        self.roof = roof
        self.tank_size = self.n_tanks * self.standard_size
        self.cur_storage = init_storage
        self.overflows = np.zeros(cfg.sim_len)


t = Tank(10, 0)
print(t.cur_storage)
print(np.zeros(100))
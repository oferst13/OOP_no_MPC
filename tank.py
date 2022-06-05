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

    def set_storage(self):
        pass

    def get_storage(self):
        pass

    def set_overflow(self):
        pass

    def get_overflow(self):
        pass

    def set_release(self):
        pass

    def tot_outflow(self):
        pass

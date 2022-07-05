import copy

import numpy as np
import cfg


class Tank:
    standard_size = 20
    standard_orifice = 0.05
    standard_diameter = 2.8
    all_tanks = []

    def __init__(self, name, n_tanks, init_storage, roof, dwellers):
        self.name = name
        self.n_tanks = n_tanks
        self.init_storage = init_storage
        self.roof = roof
        self.dwellers = dwellers
        self.tank_size = self.n_tanks * self.standard_size
        self.cur_storage = init_storage
        self.orifice_A = ((self.standard_orifice / 2) ** 2) * np.pi
        self.footprint = ((self.standard_diameter / 2) ** 2) * np.pi
        self.overflows = np.zeros(cfg.sim_len)
        self.releases = np.zeros(cfg.sim_len)
        self.rw_supply = np.zeros(cfg.sim_len)
        self.all_storage = np.zeros(cfg.sim_len)
        self.all_storage[0] = self.init_storage
        self.all_storage_temp = copy.copy(self.all_storage)
        self.inflow_forecast = None
        self.inflow_actual = None
        self.daily_demands = None  # currently with dt only
        Tank.all_tanks.append(self)

    @classmethod
    def get_tot_storage(cls):
        tot_storage: float = 0
        for tank in cls.all_tanks:
            tot_storage += tank.cur_storage
        return tot_storage

    @classmethod
    def get_tot_overflow(cls, timestep):
        tot_overflow: float = 0
        for tank in cls.all_tanks:
            tot_overflow += (tank.overflows[timestep] / cfg.dt)
        return tot_overflow

    @classmethod
    def get_cum_overflow(cls):
        cum_overflow = np.zeros(cfg.sim_len)
        for tank in cls.all_tanks:
            cum_overflow += tank.overflows
        return np.sum(cum_overflow)

    def get_overflow(self):
        pass

    def set_release(self, release_deg):
        release_Q = self.n_tanks * self.orifice_A * cfg.Cd\
                    * np.sqrt(2 * 9.81 * (self.cur_storage / (self.n_tanks * self.footprint))) * 0.1 * release_deg
        return release_Q

    def tot_outflow(self):
        pass

    def set_inflow_forecast(self, rain):
        self.inflow_forecast = rain * self.roof / 1000

    def set_daily_demands(self, demand_pattern):
        self.daily_demands = demand_pattern * self.dwellers / 1000

    def tank_fill(self, cur_rain_volume, timestep):
        self.cur_storage += cur_rain_volume
        if self.cur_storage > self.tank_size:
            overflow = self.cur_storage - self.tank_size
            self.cur_storage = self.tank_size
            self.overflows[timestep] = overflow

    def rw_use(self, demand, timestep):
        self.cur_storage -= demand
        self.rw_supply[timestep] = copy.copy(demand)
        if self.cur_storage < 0:
            self.cur_storage += demand
            self.rw_supply[timestep] = copy.copy(self.cur_storage)
            self.cur_storage = 0

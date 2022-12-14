import copy

import numpy as np
import cfg


class Tank:
    standard_size = 10
    standard_orifice = 0.05
    standard_diameter = 2.55
    all_tanks = []

    # def __init__(self, name, n_tanks, init_storage, roof, dwellers):
    def __init__(self, dictionary):
        # self.name = name
        # self.n_tanks = n_tanks
        # self.init_storage = init_storage
        # self.roof = roof
        # self.dwellers = dwellers
        for att, val in dictionary.items():
            setattr(self, att, val)

        self.tank_size = self.n_tanks * self.standard_size
        self.cur_storage = None
        self.orifice_A = ((self.standard_orifice / 2) ** 2) * np.pi
        self.footprint = ((self.standard_diameter / 2) ** 2) * np.pi
        self.overflows = None
        self.releases = None
        self.release_volume = None
        self.rw_supply = None
        self.all_storage = None
        self.inflow_forecast = None
        self.inflow_actual = None
        self.daily_demands = None  # currently with dt only
        self.reset_tank()
        Tank.all_tanks.append(self)

    @classmethod
    def get_tot_storage(cls):
        tot_storage: float = 0
        for tank in cls.all_tanks:
            tot_storage += tank.cur_storage
        return tot_storage

    @classmethod
    def get_tot_outflow(cls, timestep):
        tot_outflow: float = 0
        for tank in cls.all_tanks:
            tot_outflow += (tank.overflows[timestep] + tank.release_volume[timestep]) / cfg.dt
        return tot_outflow

    @classmethod
    def get_cum_overflow(cls):
        cum_overflow = np.zeros(cfg.sim_len)
        for tank in cls.all_tanks:
            cum_overflow += tank.overflows
        return np.sum(cum_overflow)

    @classmethod
    def get_cum_release(cls):
        cum_release = np.zeros(cfg.sim_len)
        for tank in cls.all_tanks:
            cum_release += tank.release_volume
        return np.sum(cum_release)

    @classmethod
    def get_cum_outflow(cls):
        return cls.get_cum_release() + cls.get_cum_overflow()

    @classmethod
    def get_last_overflow(cls):
        last_overflow_list = []
        for tank in cls.all_tanks:
            if np.sum(tank.overflows) > 0:
                last_overflow_list.append(np.max(np.nonzero(tank.overflows)))
        if last_overflow_list:
            return max(last_overflow_list)
        else:
            return 0

    @classmethod
    def set_inflow_forecast_all(cls, forecast_rain):
        for tank in Tank.all_tanks:
            tank.set_inflow_forecast(forecast_rain)

    @classmethod
    def set_daily_demands_all(cls, demands_pd):
        for tank in Tank.all_tanks:
            tank.set_daily_demands(demands_pd)

    def calc_release(self, timestep, last_overflow):
        if timestep <= last_overflow:
            release_deg = self.releases[timestep // int(cfg.release_dt / cfg.dt)]
        else:
            release_deg = 0.0
        release_Q = self.n_tanks * self.orifice_A * cfg.Cd \
                    * np.sqrt(2 * 9.81 * (self.cur_storage / (self.n_tanks * self.footprint))) * 0.1 * release_deg
        release_vol = release_Q * cfg.dt
        self.cur_storage -= release_vol
        self.release_volume[timestep] = copy.copy(release_vol)
        if self.cur_storage < 0.0:
            self.cur_storage += release_vol
            self.release_volume[timestep] = copy.copy(self.cur_storage)
            self.cur_storage = 0.0

    def reset_tank(self):
        self.cur_storage = self.init_storage
        self.overflows = np.zeros(cfg.sim_len)
        self.releases = np.zeros(int(cfg.sim_len / (cfg.release_dt / cfg.dt)))
        self.release_volume = np.zeros(cfg.sim_len)
        self.rw_supply = np.zeros(cfg.sim_len)
        self.all_storage = np.zeros(cfg.sim_len)
        self.all_storage[0] = self.init_storage

    def set_inflow_forecast(self, rain):
        self.inflow_forecast = rain * self.roof / 1000

    def set_daily_demands(self, demand_pattern):
        self.daily_demands = demand_pattern * self.dwellers / 1000

    def tank_fill(self, timestep):
        cur_rain_volume = self.inflow_forecast[int(timestep // (cfg.rain_dt / cfg.dt))] * (cfg.dt / cfg.rain_dt)
        self.cur_storage += cur_rain_volume
        if self.cur_storage > self.tank_size:
            overflow = self.cur_storage - self.tank_size
            self.cur_storage = self.tank_size
            self.overflows[timestep] = overflow

    def set_releases(self, release_vec):
        self.releases = release_vec

    def rw_use(self, timestep):
        demand = self.daily_demands[timestep % self.daily_demands.shape[0]]
        self.cur_storage -= demand
        self.rw_supply[timestep] = copy.copy(demand)
        if self.cur_storage < 0:
            self.cur_storage += demand
            self.rw_supply[timestep] = copy.copy(self.cur_storage)
            self.cur_storage = 0
        self.all_storage[timestep] = copy.copy(self.cur_storage)

import numpy as np
import copy

dt = 60
rain_dt = 60 * 10
beta = 5 / 4
manning = 0.012
sim_days = 1
sim_len = int(sim_days * 24 * 60 * 60 / dt)
t = np.linspace(0, sim_len, num=sim_len + 1)
t = t.astype(int)
hours = t * (dt / 60) / 60
days = hours / 24
collective_hor = True
forecast_hor = 3
if collective_hor:
    prediction_hor = copy.copy(forecast_hor)
    control_hor = copy.copy(forecast_hor)

standard_size = 20
n_tanks = np.array([30, 35, 25, 50])
tank_size = n_tanks * standard_size
tank_init_storage = np.copy(tank_size) * 0.5
tank_storage = tank_init_storage
roof = np.array([9000, 10000, 8500, 14000])
dwellers = np.array([180, 190, 150, 650])

tank_outlets = np.array([250, 330, 220, 350])
tank_Ds = np.array([0.4, 0.4, 0.4, 0.4])
tank_slopes = np.array([0.02, 0.015, 0.02, 0.007])
tank_alphas = (0.501 / manning) * (tank_Ds ** (1 / 6)) * (tank_slopes ** 0.5)

# Deterministic demands - Change if necessary!
demand_dt = 3 * 60 * 60
demands_3h = np.array([5, 3, 20, 15, 12, 15, 18, 12])
PD = 33
demands = np.array([])
for demand in demands_3h:
    demands = np.append(demands, np.ones(int(demand_dt / dt)) * (demand * (dt / demand_dt)))
demand_PD = demands * PD / 100

pipes_L = np.array([400, 500, 400, 400, 300, 200])
pipe_Ds = np.array([0.4, 0.6, 0.4, 0.8, 0.4, 0.8])
pipe_slopes = np.array([0.0063, 0.002, 0.0013, 0.0088, 0.005, 0.01])
pipe_alphas = (0.501 / manning) * (pipe_Ds ** (1 / 6)) * (pipe_slopes ** 0.5)

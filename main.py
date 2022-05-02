import numpy as np

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

standard_size = 20
n_tanks = np.array([30, 35, 25, 50])
tank_size = n_tanks * standard_size
tank_init_storage = np.copy(tank_size) * 0.5
tank_storage = tank_init_storage
roof = np.array([9000, 10000, 8500, 14000])
dwellers = np.array([180, 190, 150, 650])

demand_dt = 3 * 60 * 60
demands_3h = np.array([5, 3, 20, 15, 12, 15, 18, 12])
demands_PD = 33
demands = np.array([])
for demand in demands_3h:
    demands = np.append(demands, np.ones(int(demand_dt / dt)) * (demand * (dt / demand_dt)))
demands = demands * demands_PD / 100
demand_volume = np.matmul(np.reshape(dwellers, (len(dwellers), 1)), np.reshape(demands, (1, len(demands)))) / 1000

tank_outlets = np.array([250, 330, 220, 350])
tank_Ds = np.array([0.4, 0.4, 0.4, 0.4])
tank_slopes = np.array([0.02, 0.015, 0.02, 0.007])
tank_alphas = (0.501 / manning) * (tank_Ds ** (1 / 6)) * (tank_slopes ** 0.5)
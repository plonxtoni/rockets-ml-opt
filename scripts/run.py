import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent)) 

import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from core.config import Propellant, BatesGrainGeometry, Nozzle, CombustionModel, MotorConfig
from core.solver import simulate, make_result
from vis.plotting import plot_signal_window

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

PLOT_LINE_COLOR = 'teal'
PEAK_LINE_COLOR = 'maroon'

def status(msg, t0):
    elapsed = time.time() - t0
    print(f"  [{elapsed:.3f}s]  {msg}")

t0 = time.time()
print(" ====== Solid Motor Simulation ====== ")


status("Setting config...", t0)

# Motor configuration
propellant = Propellant(
    rho   = 1889.0,
    a     = 8.26e-5,
    n     = 0.319,
    T_c   = 1720.0,
    gamma = 1.133,
    R     = 164.0,
)

geom = BatesGrainGeometry(
    grain_type = 'bates',
    L0         = 0.10,
    r_i0       = 0.015,
    r_o        = 0.030,
)

nozzle     = Nozzle(throat_radius=0.008)
combustion = CombustionModel(eta_cstar=0.95, eta_cf=0.98)

config = MotorConfig(
    propellant = propellant,
    nozzle     = nozzle,
    geom       = geom,
    combustion = combustion,
)
status("Config built", t0)


# Initial conditions
y0     = [101325.0, 0.0]    # amb pressure, no web consumed
t_span = (0.0, 100.0)    # max time range in s

# Run simulation
status("Initiating solve...", t0)
result = simulate(t_span, y0, config, method='RK45', rtol=1e-6, atol=1e-8)
status(f"Solution complete — {len(result.t)} steps, converged={result.converged}", t0)

# Print summary of results
print("Summary of results:")
print(f"|Burn time: {result.burn_time:.3f} s            |")
print(f"-------------------------------------------------")
print(f"|Peak pressure: {result.P_c.max():.6f} Pa       |")
print(f"-------------------------------------------------")
print(f"|Peak thrust: {result.thrust.max():.1f} N       |")
print(f"-------------------------------------------------")
print(f"|Total impulse: {result.total_impulse:.1f} N·s  |")
print(f"-------------------------------------------------")
print(f"|Burned mass: {result.burned_mass*1000:.1f} g   |")
print(f"-------------------------------------------------")
print(f"|c* (actual): {result.c_star:.1f} m/s           |")
print(f"-------------------------------------------------")
print()

status("Saving results...", t0)
sim_results = make_result(result, config, P_amb=101325.0)
sim_results_save_path = f'results/data_simulation_results_{timestamp}.npy'
np.save(sim_results, sim_results_save_path, allow_pickle=True)

# Plotting
status("Plotting...", t0)
fig, ax = plt.subplots(2, 3, figsize=(15, 8), constrained_layput=True)
fig.suptitle("Solid Motor Simulation", fontweight='bold')

plot_signal_window(ax[0, 0], result.t, result.P_c, 'P_c [Pa]', 'Chamber Pressure', fmt='.3f')
plot_signal_window(ax[0, 1], result.t, result.thrust, 'Thrust [N]', 'Thrust', fmt='.1f')
plot_signal_window(ax[0, 2], result.t, result.m_dot, 'ṁ [kg/s]', 'Mass Flow Rate', fmt='.4f')
plot_signal_window(ax[1, 0], result.t, result.A_b * 1e6, 'A_b [mm²]', 'Burning Area', fmt='.2f')
plot_signal_window(ax[1, 1], result.t, result.r_i * 1e3, 'r_i [mm]', 'Inner Radius', show_peak=False)
plot_signal_window(ax[1, 2], result.t, result.L  * 1e3, 'L [mm]', 'Grain Length', show_peak=False)

plt.tight_layout()
plots_save_path = f'results/simulation_results_{timestamp}.png'
plt.savefig(plots_save_path, dpi=300)
status("Plot saved to results/plots_simulation_results.png", t0)
plt.show()
print(" ==================================== ")
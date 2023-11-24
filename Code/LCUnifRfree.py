# Import relevant packages

import calibration as parameters
import warnings  # The warnings package allows us to ignore some harmless but alarming warning messages
from estimation import estimate, plot_lorenz_dist
from calibration import SCF_wealth, SCF_weights
from HARK.utilities import get_lorenz_shares
import numpy as np
import matplotlib.pyplot as plt 

# Import related generic python packages

warnings.filterwarnings("ignore")


def mystr(number):
    return f"{number:.4f}"


# Specify parameters for options dictionary
param_name = "Rfree"  # Which parameter to introduce heterogeneity in
dist_type = "logdiff_uniform"  # Which type of distribution to use
run_estimation = True  # Runs the estimation if True
run_sensitivity = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]  # Choose which sensitivity analyses to run: rho, xi_sigma, psi_sigma, mu, urate, mortality, g, R
find_beta_vs_KY = False  # Computes K/Y ratio for a wide range of beta; should have do_beta_dist = False
do_tractable = (
    False  # Uses a "tractable consumer" rather than solving full model when True
)

# First solve without heterogeneity
do_param_dist = False  # Do param-dist version if True, param-point if False
do_lifecycle = True  # Use lifecycle model if True, perpetual youth if False
do_agg_shocks = False  # Solve the FBS aggregate shocks version of the model
do_liquid = False  # Matches liquid assets data when True, net worth data when False

options = {
    "param_name": param_name,
    "dist_type": dist_type,
    "run_estimation": run_estimation,
    "run_sensitivity": run_sensitivity,
    "find_beta_vs_KY": find_beta_vs_KY,
    "do_tractable": do_tractable,
    "do_param_dist": do_param_dist,
    "do_lifecycle": do_lifecycle,
    "do_agg_shocks": do_agg_shocks,
    "do_liquid": do_liquid,
}

EconomyPoint = estimate(options, parameters)

# Then solve with heterogeneity
do_param_dist = True  # Do param-dist version if True, param-point if False
do_lifecycle = True  # Use lifecycle model if True, perpetual youth if False
do_agg_shocks = False  # Solve the FBS aggregate shocks version of the model
do_liquid = False  # Matches liquid assets data when True, net worth data when False
do_tractable = False

options = {
    "param_name": param_name,
    "dist_type": dist_type,
    "run_estimation": run_estimation,
    "run_sensitivity": run_sensitivity,
    "find_beta_vs_KY": find_beta_vs_KY,
    "do_tractable": do_tractable,
    "do_param_dist": do_param_dist,
    "do_lifecycle": do_lifecycle,
    "do_agg_shocks": do_agg_shocks,
    "do_liquid": do_liquid,
    "do_combo_estimation": False,
}

EconomyDist = estimate(options, parameters)

pctiles = np.linspace(0.001, 0.999, 15)  # may need to change percentiles
SCF_Lorenz_points = get_lorenz_shares(
        SCF_wealth, weights=SCF_weights, percentiles=pctiles
    )

sim1_wealth = np.concatenate(EconomyPoint.reap_state["aLvl"])
sim1_weight = np.concatenate(EconomyPoint.reap_state["WeightFac"])
order = np.argsort(sim1_wealth)
sim1_wealth = sim1_wealth[order]
sim1_weight = sim1_weight[order]
sim1_Lorenz_points = get_lorenz_shares(
            sim1_wealth, weights=sim1_weight, percentiles=pctiles
        )

sim2_wealth = np.concatenate(EconomyDist.reap_state["aLvl"])
sim2_weight = np.concatenate(EconomyDist.reap_state["WeightFac"])
order = np.argsort(sim2_wealth)
sim2_wealth = sim2_wealth[order]
sim2_weight = sim2_weight[order]
sim2_Lorenz_points = get_lorenz_shares(
            sim2_wealth, weights=sim2_weight, percentiles=pctiles
        )

plt.figure(figsize=(5, 5))
plt.title("Wealth Distribution")
plt.plot(pctiles, SCF_Lorenz_points, "-k", label="SCF")
plt.plot(
        pctiles, sim1_Lorenz_points, "--k", label="R-point"
    )
plt.plot(
        pctiles, sim2_Lorenz_points, "-.k", label="R-dist"
    )
plt.xlabel("Percentile of net worth")
plt.ylabel("Cumulative share of wealth")
plt.legend(loc=2)
plt.ylim([0, 1])
    


import calibration as parameters
import warnings  # The warnings package allows us to ignore some harmless but alarming warning messages
from estimation import (estimate, plot_lorenz_dist, get_spec_name, 
                        get_param_count, set_up_economy)
import numpy as np

# Import related generic python packages

warnings.filterwarnings("ignore") 


def mystr(number):
    return f"{number:.4f}"


# Specify parameters for options dictionary
param_name = "Rfree"  # Which parameter to introduce heterogeneity in
dist_type = "uniform"  # Which type of distribution to use
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
do_lifecycle = False  # Use lifecycle model if True, perpetual youth if False
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
    "WUF": True
}

spec_name = get_spec_name(options)
param_count = get_param_count(options)
economy = set_up_economy(options, parameters, param_count)

economy.spec_name = spec_name
economy.param_count = param_count

economy.assign_parameters(LorenzBool=True, ManyStatsBool=True)
economy.distribute_params(param_name, param_count, .99, 0.0, dist_type)
economy.solve()

#economy = estimate(options, parameters)

print(economy.history)
print(economy.agents[0].Rfree)



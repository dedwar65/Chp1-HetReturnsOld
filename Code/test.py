# This will be a pedantic file which will go through the steps needed to
# produce the empirical moments for a given calibration of the model.

import numpy as np
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType
from HARK.utilities import get_lorenz_shares

########### PY point model #############
init_infinite = {
    "CRRA": 1.01,
    "Rfree": 1.01 / [1.0 - 1.0 / 160.0][0],
    "PermGroFac": [1.000**0.25],
    "PermGroFacAgg": 1.0,
    "BoroCnstArt": 0.0,
    "CubicBool": False,
    "vFuncBool": False,
    "PermShkStd": [(0.01 * 4 / 11) ** 0.5],
    "PermShkCount":5,
    "TranShkStd": [(0.01 * 4) ** 0.5],
    "TranShkCount": 5,
    "UnempPrb": 0.07,
    "IncUnemp": .15,
    "UnempPrbRet": None,
    "IncUnempRet": None,
    "aXtraMin": 0.00001,
    "aXtraMax": 20,
    "aXtraCount": 20,
    "aXtraExtra": [None],
    "aXtraNestFac": 3,
    "LivPrb": [1.0 - 1.0 / 160.0],
    "PopGroFac": 1.0,
    "DiscFac": 0.99,  # dummy value, will be overwritten
    "cycles": 0,
    "T_cycle": 1,
    "T_retire": 0,
    "T_sim": 1200,
    "T_age": 400,
    "IndL": 10.0 / 9.0,
    "aNrmInitMean": np.log(0.00001),
    "aNrmInitStd": 0.0,
    "pLvlInitMean": 0.0,
    "pLvlInitStd": 0.0,
    "AgentCount": 10000,  # will be overwritten by parameter distributor
    # Add the 6 key-value pairs to solve the Agent's problem modified to allow for bequest motives
    "BeqCRRA": 1.01,
    "BeqFac": 1.0,
    "BeqShift": 0.0,
    "TermBeqCRRA": 1.01,
    "TermBeqFac": 1.0,
    "TermBeqShift": 0.0,
}

PYpoint = IndShockConsumerType(**init_infinite)
PYpoint.solve()
PYpoint.track_vars = ["aLvl", "pLvl"]
PYpoint.initialize_sim()
PYpoint.simulate()

# simulated KY ratio
aLvl = PYpoint.history["aLvl"].flatten()
pLvl = PYpoint.history["pLvl"].flatten()

CapAgg = np.sum(aLvl)
IncAgg = np.sum(pLvl) #times the transitory shock?
KtoYsim = CapAgg / IncAgg
print(KtoYsim)

# simulated lorenz targets
order = np.argsort(aLvl)
aLvl = aLvl[order]
LorenzSim = get_lorenz_shares(
                aLvl,
                percentiles=[0.2, 0.4, 0.6, 0.8],
                presorted=True,
            )



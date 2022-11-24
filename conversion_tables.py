import numpy as np
import pandas as pd

from ixdat.constants import R, STANDARD_TEMPERATURE as T, STANDARD_PRESSURE as P
from EC_MS.Chem import get_drG

SECONDS_IN_HOUR = 3600
HOURS_IN_YEAR = 24 * 365
kJ_IN_MWh = SECONDS_IN_HOUR * 1e3

MOLAR_MASSES = {"H2": 2e-3, "CH4": 16e-3, "NH3": 17e-3}    # molar mass in [kg/mol]
MOLAR_ENERGIES = {
    "H2": -get_drG("2 H2 + O2 -> 2 H2O") / 2,
    "CH4": -get_drG("CH4 + 2 O2 -> CO2 + 2 H2O"),
    "NH3": -get_drG("4 NH3 + 3 O2 -> 6 H2O + 2 N2", dfG={'NH3': -16.5}) / 4,
}  # delta G of combustion, [kJ/mol]
DENSITIES = {
    "H2": MOLAR_MASSES["H2"] * P / (R * T),
    "CH4": MOLAR_MASSES["CH4"] * P / (R * T),
    "NH3": MOLAR_MASSES["NH3"] * P / (R * T),
}  # density of gas at standard conditions in [kg/m^3]

SPECIFIC_ENERGIES = {
    "H2": MOLAR_ENERGIES["H2"] / MOLAR_MASSES["H2"],
    "CH4": MOLAR_ENERGIES["CH4"] / MOLAR_MASSES["CH4"],
    "NH3": MOLAR_ENERGIES["NH3"] / MOLAR_MASSES["NH3"]
}  # energy in kJ / kg
VOLUMETRIC_ENERGIES = {
    "H2": MOLAR_ENERGIES["H2"] * P / (R * T),
    "CH4": MOLAR_ENERGIES["CH4"] * P / (R * T),
    "NH3": MOLAR_ENERGIES["NH3"] * P / (R * T),
}  # energy in kJ / m^3

one_megawatt = {
    "MW": 1,
    "GWh/yr": HOURS_IN_YEAR / 1000,
    "kg(H2)/hr": kJ_IN_MWh / SPECIFIC_ENERGIES["H2"],
    "ton(H2)/yr": kJ_IN_MWh / SPECIFIC_ENERGIES["H2"] * HOURS_IN_YEAR / 1000,
    "m^3(CH4)/hr": kJ_IN_MWh / VOLUMETRIC_ENERGIES["CH4"],
    "1000 m^3(CH4)/yr": kJ_IN_MWh / VOLUMETRIC_ENERGIES["CH4"] * HOURS_IN_YEAR / 1000,
    "kg(NH3)/hr": kJ_IN_MWh / SPECIFIC_ENERGIES["NH3"],
    "t(NH3)/yr": kJ_IN_MWh / SPECIFIC_ENERGIES["NH3"] * HOURS_IN_YEAR / 1000,
}
columns = list(one_megawatt.keys())
one_GWhpy = {
    name: value / one_megawatt["GWh/yr"] for name, value in one_megawatt.items()
}
values_for_table = np.array([
    [value / one_megawatt[name] for value in one_megawatt.values()]
    for name in columns
])

df = pd.DataFrame(values_for_table, columns=columns)

df.to_csv("conversions by energy content.csv")

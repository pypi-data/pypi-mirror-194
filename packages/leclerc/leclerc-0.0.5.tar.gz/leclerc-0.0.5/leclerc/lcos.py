# Based on formula:
# https://eudl.eu/pdf/10.4108/eai.13-7-2018.155643#:~:text=The%20LCOS%20is%20determined%20as
# "Calculation of the Levelised Cost of Electrical Energy Storage for Short-Duration Application.
# LCOS Sensitivity Analysis "
from leclerc.montecarlinator import pert_monte_carlo, PERT

# Import unit testing stuff
import unittest
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt


# Calculate the levelized cost of storage (LCOS) for a given storage system
# Inputs:
#   inflation: inflation rate
#   discount_rate: discount rate
#   electricity_correction_coefficient: electricity correction coefficient
#   cap_total: total capacity of the storage system
#   o_m_yearly: yearly operating and maintenance cost
def lcos(
		useful_life,
		nominal_discount_rate,
		inflation_rate,
		capacity_MWh,
		capital_cost,
		cycles_per_year,
		max_depth_of_discharge_fraction,
		degradation_fraction,
		energy_input_price,
		round_trip_efficiency,
		fixed_o_m_costs_yearly,
):
	
	real_discount_rate = (1+(nominal_discount_rate/100))/(1+(inflation_rate/100))-1
	present_value_fixed_o_m = -1.0* npf.pv(real_discount_rate, useful_life, fixed_o_m_costs_yearly, 0)
	
	# Annuity factor
	annuity_factor= (1-((1-degradation_fraction)/(1+real_discount_rate))**useful_life)/(real_discount_rate+degradation_fraction)

	# Present value of energy generation
	present_value_energy_generation = capacity_MWh * cycles_per_year * max_depth_of_discharge_fraction *  annuity_factor #might want to multiply by (1 - degradation_fraction) *

	# Overnight Capital is PV of capital cost / PV of energy generation
	overnight_capital = capital_cost / present_value_energy_generation

	# Fixed O&M is PV of fixed O&M / PV of energy generation
	fixed_o_m = present_value_fixed_o_m / present_value_energy_generation
	adjusted_energy_price = energy_input_price / round_trip_efficiency

	# Total LCOS including energy input
	lcos = overnight_capital+fixed_o_m+adjusted_energy_price

	return lcos


# Probabilistic version based on pert wrapper. This is a wrapper around the deterministic function above.
# This function takes in PERT distributions for any of the inputs and returns a distribution for the output.
@pert_monte_carlo
def probabilistic_lcos(
	calculation,
	name,
	useful_life,
	nominal_discount_rate,
	inflation_rate,
	capacity_MWh,
	capital_cost,
	cycles_per_year,
	max_depth_of_discharge_fraction,
	degradation_fraction,
	energy_input_price,
	round_trip_efficiency,
	fixed_o_m_costs_yearly,
):
	return lcos(
		useful_life,
		nominal_discount_rate,
		inflation_rate,
		capacity_MWh,
		capital_cost,
		cycles_per_year,
		max_depth_of_discharge_fraction,
		degradation_fraction,
		energy_input_price,
		round_trip_efficiency,
		fixed_o_m_costs_yearly,
	)

class Testing(unittest.TestCase):
	def test_lithium(self):
		result = lcos(
			useful_life=20,
			nominal_discount_rate=0.08,
			inflation_rate=0.02,
			capacity_MWh=42000,
			capital_cost=9660000000,
			cycles_per_year=365,
			max_depth_of_discharge_fraction=1,
			degradation_fraction=0.01,
			energy_input_price=12,
			round_trip_efficiency=0.95,
			fixed_o_m_costs_yearly=59985000,
		)
		expected = 76
		self.assertAlmostEqual(result, expected, places=0)

	def test_flow(self):
		result = lcos(
			useful_life=25,
			nominal_discount_rate=0.08,
			inflation_rate=0.02,
			capacity_MWh=42000,
			capital_cost=6165000000,
			cycles_per_year=365,
			max_depth_of_discharge_fraction=1,
			degradation_fraction=0.0,
			energy_input_price=12,
			round_trip_efficiency=0.65,
			fixed_o_m_costs_yearly=123300000,
		)
		expected = 58
		self.assertAlmostEqual(result, expected, places=0)

if __name__ == "__main__":
	lcos_results = probabilistic_lcos("LCOS", "AAPL - SF 100% Li Tesla", 40, 8, PERT(min=1, mode=2, max=3, label="Inflation"), 50505, 15832712080, 273, 1, 0.0148, 20, 0.931, 139416958.7)
	lcos_results = probabilistic_lcos("LCOS", "AAPL -SF 100% Li SAFT", 20, 8, PERT(min=1, mode=2, max=4, label="Inflation"), 49766, 9790564710, 273, 0.95, 0.0171, 20, 0.931, 195811294)
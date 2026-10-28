"""
Main file for the HYRAILOS Python case study.

Run this file to start the simulation. First-time users should modify only the settings dictionary below 
to choose the train structure, time window, FMU, catenary availability, optimization parameters,
solver, and plotting options.
"""

import idaes  # Initialize the IDAES solver search path.
from pyomo.environ import SolverFactory

from simulation import run_simulation
from data_carriage import (
    load_carriage_data_1,
    load_carriage_data_2,
    load_carriage_data_a1,
    load_carriage_data_a2,
)

"""
===============================================================================
USER GUIDE

This script is the main file to simulate the overall train operation.

➡️ The user can modify the 'settings' dictionary below.

You can:
- Change traction current reference (but you need to have one)
- Modify train configuration (number and type of carriages)
- Tune FMU sampling time, as well as time window to simulate
- Tune MPC parameters and weights of the cost function
- Select solver and simulation options

Then simply run this script. At the end, the results will be plotted.
===============================================================================
"""

settings = {

    # -------------------------------------------------------------------------
    # INPUT
    # -------------------------------------------------------------------------
    # Path to the traction current reference file (.mat format)
    #
    # Expected format:
    #   - 2 columns (no header)
    #   - Column 1: time [seconds]
    #   - Column 2: traction current [A]
    #
    # Time must be discretized consistently with the simulation.
    "traction_current_path": "Traction_current_reference.mat",

    # -------------------------------------------------------------------------
    # TRAIN CONFIGURATION
    # -------------------------------------------------------------------------
    # Define the type of each carriage:
    #   "t" → traction carriage (contains all components)
    #   "a" → auxiliary carriage (contains only auxiliary services)
    #
    # Working example below: 4-car train → traction + auxiliary + auxiliary + traction
    "car_types": ["t", "a", "a", "t"],

    # Carriage data (must match the order of 'car_types')
    # (Example of data: resistances, inductances, capacitances, voltages, states of charge, ...)
    "data": [
        load_carriage_data_1(),
        load_carriage_data_a1(),
        load_carriage_data_a2(),
        load_carriage_data_2(),
    ],

    # Define to which carriage the catenary is connected (0 means no catenary connection at all)
    "cat_pos": 1,
    # Time intervals (in minutes) where the catenary is available
    #
    # Example:
    #   (0, 19)   → catenary available from minute 0 to 19
    #   (61, 99)  → ON again
    #   (161,195) → ON again
    #
    # Outside these intervals → train runs in catenary-free section
    #
    # Leave void [] if no catenary is connected
    "catenary_intervals": [(0, 19), (61, 99), (161, 195)],

    # -------------------------------------------------------------------------
    # FMU (PLANT MODEL)
    # -------------------------------------------------------------------------
    # Path to the Functional Mock-up Unit (FMU) describing the train model
    "fmu_path": "FourCarriagesFMU.fmu",
    # For Linux users, they have to use the "FourCarriagesFMU_Linux.fmu" instead

    # Constant averaged efficiency used by every onboard DC/DC converter.
    "converter_efficiency": 0.97,

    # -------------------------------------------------------------------------
    # SIMULATION TIME SETTINGS
    # -------------------------------------------------------------------------
    "t_start": 0, # Start time [minutes], minimum value in this case: 0
    "t_end": 195, # End time [minutes], maximum value in this case: 195
    "tau_s": 0.5, # Integration step of the FMU [seconds] (too large can create numerical problems)

    # -------------------------------------------------------------------------
    # MODEL PREDICTIVE CONTROL (MPC) SETTINGS
    # -------------------------------------------------------------------------
    "tau_s_MPC": 60, # MPC sampling time [seconds]
    "N": 30, # Prediction horizon length

    # -------------------------------------------------------------------------
    # COST FUNCTION WEIGHTS (MPC AND OFFLINE DP)
    # -------------------------------------------------------------------------
    # These weights define the trade-off in the optimization problem
    #
    # wfc → penalty on fuel cell usage
    # wb  → penalty on battery usage
    # wsc → penalty on supercapacitor usage
    # wcat → penalty on current injected back to the catenary
    # Higher value → stronger penalization
    "wfc": 1e2,
    "wb": 1,
    "wsc": 1e1,
    "wcat": 1e3,

    # -------------------------------------------------------------------------
    # SOLVER SETTINGS
    # -------------------------------------------------------------------------
    # IPOPT is used for nonlinear optimization (via Pyomo)
    #
    # Make sure IPOPT is installed and accessible in your environment
    "solver": SolverFactory("ipopt"),

    # -------------------------------------------------------------------------
    # OUTPUT / VISUALIZATION
    # -------------------------------------------------------------------------
    # If True → simulation results will be plotted automatically
    "plot_results": True,

    # If True → every generated PDF is overwritten automatically at each run.
    # Relative paths are resolved from this Case_Study_Simulation directory.
    "save_figures": True,
    "figures_output_dir": "Results/Figures",
}

# =============================================================================
# RUN SIMULATION
# =============================================================================
# The function 'run_simulation' takes the settings dictionary and:
#   - Loads input data
#   - Initializes the FMU model
#   - Solves and simulates DP
#   - Runs the MPC controller
#   - Runs LPF-EMS
#   - Simulates the full system
#   - Returns results
results = run_simulation(settings)

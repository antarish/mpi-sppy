c#!/bin/bash
#python ../agnostic_cylinders.py --module-name farmer4agnostic --default-rho 1 --num-scens 3 --solver-name cplex --guest-language Pyomo
# NOTE: you need the AMPL solvers!!!
python ../agnostic_cylinders.py --module-name mpisppy.agnostic.examples.steel_ampl_model --default-rho 1 --num-scens 3 --seed 17 --solver-name gurobi --guest-language AMPL --ampl-model-file steel.mod --ampl-data-file steel.dat
#could i ad a -- data file name 

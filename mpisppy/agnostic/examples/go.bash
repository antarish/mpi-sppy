#!/bin/bash
#python ../agnostic_cylinders.py --module-name farmer4agnostic --default-rho 1 --num-scens 6 --solver-name gurobi --guest-language Pyomo  --max-iterations 1

#python ../agnostic_cylinders.py --module-name farmer4agnostic --default-rho 1 --num-scens 6 --solver-name gurobi --guest-language Pyomo --max-iterations 1 --bundle-size 3 

#mpiexec -np 3 python ../agnostic_cylinders.py --module-name farmer4agnostic --default-rho 1 --num-scens 6 --solver-name gurobi --guest-language Pyomo --xhatshuffle --lagrangian --max-iterations 10 --rel-gap .01

#mpiexec -np 3 python ../agnostic_cylinders.py --module-name farmer4agnostic --default-rho 1 --num-scens 6 --solver-name gurobi --guest-language Pyomo --bundle-size 3 --xhatshuffle --lagrangian --max-iterations 10 --rel-gap .01

#python ../agnostic_cylinders.py --module-name farmer4agnostic --default-rho 1 --num-scens 3 --solver-name gurobi --guest-language Pyomo
# NOTE: you need the AMPL solvers!!!
python ../agnostic_cylinders.py --module-name mpisppy.agnostic.examples.farmer_ampl_model --default-rho 1 --num-scens 3 --solver-name gurobi --guest-language AMPL --ampl-model-file ../../../examples/farmer/farmer.mod #changed it from farmer.mod

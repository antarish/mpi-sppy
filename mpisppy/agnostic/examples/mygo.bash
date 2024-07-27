#!/bin/bash
# NOTE: you need the AMPL solvers!!!
ampl_data_file="steel.dat"
python ../agnostic_cylinders.py --module-name mpisppy.agnostic.examples.steel_ampl_model --default-rho 1 --num-scens 3 --seed 17 --solver-name HiGHS --guest-language AMPL --ampl-model-file steel.mod --ampl-data-file "$ampl_data_file"
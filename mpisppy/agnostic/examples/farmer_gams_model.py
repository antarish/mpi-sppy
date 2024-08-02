LINEARIZED = True

import os
import gams
import gamspy_base

this_dir = os.path.dirname(os.path.abspath(__file__))
gamspy_base_dir = gamspy_base.__path__[0]

import pyomo.environ as pyo
import mpisppy.utils.sputils as sputils

# for debugging
from mpisppy import MPI
fullcomm = MPI.COMM_WORLD
global_rank = fullcomm.Get_rank()

from mpisppy.agnostic import gams_guest
import mpisppy.agnostic.farmer4agnostic as farmer

def nonants_name_pairs_creator():
    return [("crop", "x")]


def stoch_param_name_pairs_creator():
    return [("crop", "yield")]


def scenario_creator(scenario_name, new_file_name, nonants_name_pairs, cfg=None):
    """ Create a scenario for the (scalable) farmer example.
    
    Args:
        scenario_name (str):
            Name of the scenario to construct.
        use_integer (bool, optional):
            If True, restricts variables to be integer. Default is False.
        sense (int, optional):
            Model sense (minimization or maximization). Must be either
            pyo.minimize or pyo.maximize. Default is pyo.minimize.
        crops_multiplier (int, optional):
            Factor to control scaling. There will be three times this many
            crops. Default is 1.
        num_scens (int, optional):
            Number of scenarios. We use it to compute _mpisppy_probability. 
            Default is None.
        seedoffset (int): used by confidence interval code

    """
    assert new_file_name is not None
    stoch_param_name_pairs = stoch_param_name_pairs_creator()

    ws = gams.GamsWorkspace(working_directory=this_dir, system_directory=gamspy_base_dir)

    ### Calling this function is required regardless of the model
    # This function creates a model instance not instantiated yet, and gathers in glist all the parameters and variables that need to be modifiable
    mi, job, nonant_set_sync_dict, stoch_sets_sync_dict, glist, all_ph_parameters_dicts, xlo_dict, xup_dict, x_out_dict = gams_guest.pre_instantiation_for_PH(ws, new_file_name, nonants_name_pairs, stoch_param_name_pairs)

    opt = ws.add_options()
    opt.all_model_types = cfg.solver_name
    if LINEARIZED:
        mi.instantiate("simple using lp minimizing objective_ph", glist, opt)
    else:
        mi.instantiate("simple using qcp minimizing objective_ph", glist, opt)

    ### Calling this function is required regardless of the model
    # This functions initializes, by adding records (and values), all the parameters that appear due to PH
    gams_guest.adding_record_for_PH(nonants_name_pairs, nonant_set_sync_dict, cfg, all_ph_parameters_dicts, xlo_dict, xup_dict, x_out_dict)

    ### This part is model specific, we define the values of the stochastic parameters depending on scenario_name
    scennum = sputils.extract_num(scenario_name)
    assert scennum < 3, "three scenarios hardwired for now"
    y = mi.sync_db.get_parameter("yield")

    if scennum == 0:  # below
        y.add_record("wheat").value = 2.0
        y.add_record("corn").value = 2.4
        y.add_record("sugarbeets").value = 16.0
    elif scennum == 1: # average
        y.add_record("wheat").value = 2.5
        y.add_record("corn").value = 3.0
        y.add_record("sugarbeets").value = 20.0
    elif scennum == 2: # above
        y.add_record("wheat").value = 3.0
        y.add_record("corn").value = 3.6
        y.add_record("sugarbeets").value = 24.0    

    return mi, nonants_name_pairs, nonant_set_sync_dict

        
#=========
def scenario_names_creator(num_scens,start=None):
    return farmer.scenario_names_creator(num_scens,start)


#=========
def inparser_adder(cfg):
    farmer.inparser_adder(cfg)

    
#=========
def kw_creator(cfg):
    # creates keywords for scenario creator
    #kwargs = farmer.kw_creator(cfg)
    kwargs = {}
    kwargs["cfg"] = cfg
    #kwargs["nonants_name_pairs"] = nonants_name_pairs_creator()
    return kwargs


#============================
def scenario_denouement(rank, scenario_name, scenario):
    # doesn't seem to be called
    if global_rank == 1:
        x_dict = {}
        for x_record in scenario._agnostic_dict["scenario"].sync_db.get_variable('x'):
            x_dict[x_record.get_keys()[0]] = x_record.get_level()
        print(f"In {scenario_name}: {x_dict}")
    pass
    # (the fct in farmer won't work because the Var names don't match)
    #farmer.scenario_denouement(rank, scenario_name, scenario)

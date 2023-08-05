"""
CLI for Lemmings
"""

import os
import click

@click.group()
def cli():
    """
    *Creation of the group that contains all cli commands.*
    """
    pass

@cli.command('run')
@click.argument('workflow', type=str, nargs=1)
@click.option('--enable-queues-from-yaml', '-eqfy', required=False, is_flag=True,
    help = "Allows user control of job and pjob queue from {workflow}.yml."
            +" This will override the queues section of your machine farming file")
def lemmings_cli(workflow, enable_queues_from_yaml):
    """ Launch farming mode of lemmings
        'lemmings-farming run {workflow_name}'
    """

    run_confirm = input("You're about to start a farming of lemmings chains." +
                        " Are you sure? (yes/no)  ").split(' ')[0]
    if run_confirm != 'yes':
        print("Aborting farming")
        return
    print()
    print("#---Starting farming mode---#")

    import sys
    import importlib.util
    from lemmings_hpc.cli_helper import (
        get_workflow_py,
        get_workflow_yml,
        custom_name,
        check_cpu_input,
    )

    from lemmings_hpc.chain.database import Database
    from lemmings_hpc.chain.machine import Machine
    from lemmings_hpc.chain.chain import Lemmings
    from lemmings_hpc.chain.lemmingjob_base import LemmingsStop
    from lemmings_hpc.chain.chain import _handle_exception
    
    #pylint: disable=too-many-function-args

    #-----default params-----------------------#
    status = 'start' # in farming mode is default,
                     # used for LemmingJob init
    user_machine = None
    #------------------------------------------#

    if enable_queues_from_yaml:
        # In this case, we do not need full check of queues in Machine init
        # use this keyword to enforce this
        user_machine = 'farming_custom_machine'

    #get path of the WorkFlow desired
    if workflow.lower().endswith(('.yml', '.py')):
        raise ValueError("A workflow name can't contain an extension like '.yml', "
                         + "please enter a valid workflow name. ")

    # Note: can probably centralise some of the checks as similar to 'lemmings run'
    try:
        wf_py_path = get_workflow_py(workflow)
    except EnvironmentError as error:
        print("EnivironmentError", error)
        return
 
    # CURRENTLY NOT ALLOWING (JJH 1/9/2021) user yaml def as not sure it's relevant in farming
    try:
    #     if yaml is not None:
    #         wf_yml_path = get_workflow_yml(yaml.split('.yml')[0], user_yaml = True)
    #     else:
        wf_yml_path = get_workflow_yml(workflow)
    except FileNotFoundError as error:
        print("FileNotFoundError: \n", error)
        return

    # Let's initialise a database
    print("Initialise farming database.yml")
    database = Database()

    chain_name = custom_name()

    try:
        print("Checking {machine}.yml")
        machine = Machine(path_yml = wf_yml_path,
                          chain_name = chain_name,
                          user_machine = user_machine)
    except EnvironmentError as excep:
        print("\nThe initialisation of Lemmings went wrong:\n")
        print("   -->  " + str(excep) + '\n')
        return
    except KeyError as excep:
        print("\nThe initialisation of Lemmings went wrong:\n", excep)
        return

    try:
        database.initialise_new_chain(machine.job_name)
        check_cpu_input(machine.user.cpu_limit)
    except ValueError as excep:
        print("\nThe initialisation of Lemmings went wrong:\n", excep)
        return
    except AttributeError as excep:
        print("\nThe initialisation of Lemmings went wrong:\n AttributeError:"+
                " keyword cpu_limit not defined in .yml file\n")
        return

    loop_count = database.count

#     # add explicitly in first loop of chain the machine path if user defined
#     # current loop important in case of restart
#     if user_machine is not None:
#         database.update_current_loop("user_machine",os.path.abspath(user_machine))

    if wf_py_path is not None:
        spec = importlib.util.spec_from_file_location("module.name",
                                                      wf_py_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        lemming_job = module.LemmingJob(workflow,
                                        machine,
                                        loop_count,
                                        status=status,
                                        cpu_limit=machine.user.cpu_limit)

    lemmings = Lemmings(lemming_job)

    try:
        # consider adding more function calls here instead of in chain.py!
        lemmings.create_replicate_workflows()
    except LemmingsStop as stop:
        _handle_exception(lemmings.lemmings_job,lemmings.database,
                        stop, lemmings_stop= True)
        print(stop) # required to know what went wrong during cli call


@cli.command('kill')
def lemmings_kill():
    """
        Kills all active Workflows.
    """

    import os
    import yaml
    from lemmings_hpc.chain.database import Database
    from lemmings_hpc.cli_helper import kill_chain

    if not os.path.isfile('database.yml'):
        print("ERROR: Can't use this command")
        print('       no database.yml file in the current directory.')
        return

    database = Database()

    # First check that we are in the correct directory to launch this command
    try:
        par_dict, = database.get_current_loop_val('parallel_runs')
    except KeyError:
        print("ERROR: this command can't be called from this directory")
        print("       Try 'lemmings kill' instead")
        return

    kill_confirm = input("Are you sure you want to kill all " 
                        + "lemmings Workflows? (yes/no)  ").split(' ')[0]

    env_var = dict(os.environ)
    try: # need to know how to kill jobs
        machine_path = env_var["LEMMINGS_MACHINE"]
    except KeyError:
        print("No LEMMINGS_MACHINE environment variable specified")
        return

    with open(machine_path) as fin:
        machine_dict = yaml.load(fin, Loader=yaml.SafeLoader)

    # check first if there is any chain to kill    
    workflows_to_kill = [key for key, val in par_dict.items() if val == 'start']
    if not workflows_to_kill:
        print("No workflows to kill")
        return

    # we have to do two things:
    #   1) update status from jobs that are waiting to killed "K"
    #   2) kill the jobs that are running

    # Change status of jobs that haven't been launched yet to 'kill'
    par_dict = dict([(key,val) if val != 'wait' else (key, 'kill')
                        for key, val in par_dict.items() ])
    database.update_current_loop('parallel_runs',[par_dict])

    main_dir = os.getcwd()
    for wf_dir in workflows_to_kill:
        os.chdir(wf_dir)
        kill_chain(database, machine_dict)
        os.chdir(main_dir)

    # now we'll update the database as we successfully killed the active chains
    par_dict = dict([(key,val) if val != 'start' else (key, 'kill')
                        for key, val in par_dict.items() ])
    database.update_current_loop('parallel_runs',[par_dict])






# @cli.command('safestop')
# def lemmings_safestop():
#     """
#     Lemmings finish properly the current loop and stop.
#     """
#     from lemmings_hpc.chain.database import Database
    
#     database = Database()
#     database.update_loop('safe_stop', True, 0) #latest


# @cli.command('endlog')
# # @click.option("--job", "-j", type=str, default=None,
# #               help="The job name you want to show")
# def lemmings_endlog():
#     """
#     Show the lemmings log of the actual/most_recent job upon finishing.
#     """
#     import os
#     from lemmings_hpc.chain.database import Database
#     db = Database()
#     # database = db._database
#     chain_name = db.latest_chain_name
#     if chain_name is None:
#         print("No lemmings database found. Check your current directory...")
#     else:
#         with open(os.path.join(chain_name, chain_name + ".log"), 'r') as fin:
#             print(fin.read())

@cli.command('status')
@click.option("--database", "-db", required=False , type=str, default = None,
              help="Path to database  YAML file (or directory) to read")
@click.option("--progress", '-p', is_flag=True,
              help="If activated, the latest progress will also be shown.")
def lemmings_status(database, progress):
    """
        Show the status during runtime
    """
    from lemmings_hpc.chain.database import Database

    try:
        if database is not None:
            if os.path.isdir(database): # try find database.yml in directory
                database = os.path.join(database, 'database.yml')
            if not os.path.isfile(database):
                raise FileNotFoundError(database + " does not exist")
        else:
            if not os.path.isfile("database.yml"):
                raise FileNotFoundError("database.yml does not exist")
    except FileNotFoundError as excep:
        print("Error: ", excep)
        return

    if database is not None:
        db = Database(database)
    else:
        ## this init will generate a database.yml file,
        ## so if not present we should check before
        db = Database()

    # First check that we are in the correct directory to launch this command
    try:
        par_dict, = db.get_current_loop_val('parallel_runs')
    except KeyError:
        print("ERROR: this command can't be called from this directory")
        print("       Try 'lemmings status' instead")
        return

    try:
        # TODO: split get_current_status in two function calls -> farming and normal
        _ = [print(string) for string in db.get_current_status(with_progress = progress)]
    except ValueError as excep:
        print("ValueError:", excep)
        return
    except TypeError as excep:
        print("Database currently not accessible, try again shortly")
        print("Make sure it is not corrupted")
        return # might be that database chain not found instead!!!
    except KeyError as excep:
        print("Database currently not accessible, try again shortly")
        return


# # @cli.command('get_tuto_files')
# # def lemmings_get_tuto():
# #     """
# #     Recover tuto lemmings/barbatruc files
# #     """
# #     import os
# #     import shutil
# #     from pathlib import Path
# #     from pkg_resources import resource_filename
# #     tuto_path = Path(resource_filename('lemmings', "")) / "example" / "barbatruc"
# #     shutil.copytree(tuto_path, os.getcwd() + '/tuto_lemmings')

@cli.command('clean')
@click.option("--database", "-db", required=False , type=str, default = None,
              help="Path to database  YAML file to read")

def lemmings_clean(database):
    """
        Clean lemmings run files in current folder
    """
    import os
    import sys
    from lemmings_hpc.cli_helper import remove_files_folders, gather_default_files_folders_to_clean
    # need to add option to have other database.yml name to look at
    # cfr. lemmings status of FEATURE/parallel branch

    try:
        lst_remove, db = gather_default_files_folders_to_clean(database, farming = True)
    except FileNotFoundError as excep:
        print("Error: ", excep)
        return
    except KeyError as excep:
        if 'use lemmings clean' in str(excep):
            return
    try:
        par_dict, = db.get_current_loop_val('parallel_runs')
        lst_remove.extend(list(par_dict))
    except KeyError:
        pass

    for path in lst_remove:
        remove_files_folders(path)


# @cli.command('info')
# @click.option("--queues", "-q", is_flag=True,
#               help="Get {machine}.yml queues info")

# def lemmings_info(queues):
#     import os
#     import yaml
#     if queues:
#         env_var = dict(os.environ)
#         try:
#             machine_path = env_var["LEMMINGS_MACHINE"]
#         except KeyError:
#             print("No LEMMINGS_MACHINE environment variable specified")
#             return

#         print("Path to {machine}.yml file", machine_path)
#         with open(machine_path) as yaml_in:
#             tmp = yaml.load(yaml_in, Loader=yaml.FullLoader)
#             print("Queues available in {machine}.yml file:")
#             for line in tmp['queues']:
#                 print("\t"+line)

#Main function called by setup.py
main = click.CommandCollection(sources=[cli], help="This is the help of lemmings-farming")

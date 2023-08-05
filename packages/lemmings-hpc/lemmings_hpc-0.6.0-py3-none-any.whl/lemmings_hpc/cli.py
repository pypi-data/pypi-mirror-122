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
@click.option("--status", "-s", type=str, default="start",
              help="Your job status, Expert users only")
@click.option('--yaml', required=False, type=str, default = None,
              help = "Path to .yml file associated with workflow")
@click.option("--noverif", is_flag=True)
@click.option("--restart", is_flag=True,
              help="If activated, the last chain will be continued.")
@click.option('--job-prefix', required=False, type=str, default = None,
   help = "Job prefix to be used in chain name. Will be prioritised over the {workflow}.yml file")
@click.option('--machine-file', required=False, type=str, default = None,
    help = "Allows user specification of  path to {machine}.yml file. "
    +"This will totally override your machine file  $LEMMINGS_MACHINE")
@click.option("--no-machine-copy", is_flag=True,
        help = "Allows user to deactivate the local copy of the {machine}.yml "
        +"file and retrieve the original working of lemmings.")
def lemmings_cli(workflow, status, yaml, noverif, restart, job_prefix,
                    machine_file, no_machine_copy):
    """
    This is the command to launch your workflow with Lemmings.
    ' lemmings run {workflow_name} '
    """

    #--Default params----------#
    local_machine_copy = True #will locally copy the used queue and commands
    #--------------------------#

    if machine_file is not None:
        # In this case we do not need a copy
        local_machine_copy = False

    if no_machine_copy:
        local_machine_copy = False

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

    #get path of the WorkFlow desired
    if workflow.lower().endswith(('.yml', '.py')):
        raise ValueError("A workflow name can't contain an extension like '.yml', "
                         + "please enter a valid workflow name. ")
#                         + "You can use the 'lemmings info workflows' "
#                        + "command to see available workflows")

    try:
        wf_py_path = get_workflow_py(workflow)
    except EnvironmentError as error:
        print("EnivironmentError", error)
        return

    try:
        if yaml is not None:
            wf_yml_path = get_workflow_yml(yaml.split('.yml')[0], user_yaml = True)
        else:
            wf_yml_path = get_workflow_yml(workflow)
    except FileNotFoundError as error:
        print("FileNotFoundError: \n", error)
        return

    database = Database()

    # if we are at a restart we wish to continue the exisiting chain
    # therefore we will overwrite the status to something else
    # a new loop must also be initiated
    if restart:
        status = "restart"
        database.initialise_new_loop()
        database.update_current_loop('restart',
                                           True)

    if status == "start":
        chain_name = custom_name()
    else:
        chain_name = database.latest_chain_name.split("_")[-1]
        # database.initialise_new_loop()

    try:
        machine = Machine(path_yml = wf_yml_path,
                          chain_name = chain_name,
                          user_machine = machine_file,
                          local_machine_copy = local_machine_copy)

        if job_prefix is not None and job_prefix not in ['None', 'none']:
            machine.job_name = job_prefix+'_'+chain_name
            machine.pjob_name = job_prefix+'_pj_'+chain_name

    # except FileNotFoundError as file_error:
    #     print("\nThe initialisation of Lemmings went wrong:\n", file_error)
    except EnvironmentError as excep:
        print("\nThe initialisation of Lemmings went wrong:\n")
        print("   -->  " + str(excep) + '\n')
        return
        #sys.exit() # look into replacing this with return!
    except KeyError as excep:
        print("\nThe initialisation of Lemmings went wrong:\n", excep)
        return
        #sys.exit()

    # put status back to start so lemmings know what to do in the chain
    if restart:
        status = "start"

    if status == "start":
        try:
            if not restart:
                database.initialise_new_chain(machine.job_name)
                print("Starting chain named " + machine.job_name)
            else:
                print("Continue chain named " + machine.job_name)
            if not noverif:
                check_cpu_input(machine.user.cpu_limit)
        except ValueError as excep:
            print("\nThe initialisation of Lemmings went wrong:\n", excep)
            return
        except AttributeError as excep:
            print("\nThe initialisation of Lemmings went wrong:\n AttributeError: keyword cpu_limit not defined in .yml file\n")
            return

    loop_count = database.count

    # add explicitly in first loop of chain the machine path if user defined
    # current loop important in case of restart
    if status == 'start' and not restart:
        if not no_machine_copy:
            # Will add this both if --user-machine and in a normal run
            database.update_current_loop("used_machine", os.path.abspath(machine.path_machine))

        database.update_first_loop("local_machine_copy", local_machine_copy)

    # if user_machine is not None:
    #     database.update_current_loop("used_machine",os.path.abspath(user_machine))

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
    lemmings.run()

@cli.command('kill')
def lemmings_kill():
    """ 
        Kill the current job and pjob of lemmings
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
        print("ERROR: this command can't be called from this directory")
        print("       Try 'lemmings-farming kill' instead")
        return
    except KeyError:
        # we are indeed in a normal lemmings chain
        pass

    env_var = dict(os.environ)
    try: # need to know how to kill jobs
        machine_path = env_var["LEMMINGS_MACHINE"]
    except KeyError:
        print("No LEMMINGS_MACHINE environment variable specified")
        return


    with open(machine_path) as fin:
        machine_dict = yaml.load(fin, Loader=yaml.SafeLoader)

    kill_chain(database, machine_dict)






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
              help="Path to database  YAML file to read")
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
        print("ERROR: this command can't be called from this directory")
        print("       Try 'lemmings-farming status' instead")
        return
    except KeyError:
        pass

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


# @cli.command('get_tuto_files')
# def lemmings_get_tuto():
#     """
#     Recover tuto lemmings/barbatruc files
#     """
#     import os
#     import shutil
#     from pathlib import Path
#     from pkg_resources import resource_filename
#     tuto_path = Path(resource_filename('lemmings', "")) / "example" / "barbatruc"
#     shutil.copytree(tuto_path, os.getcwd() + '/tuto_lemmings')

@cli.command('clean')
@click.option("--database", "-db", required=False , type=str, default = None,
              help="Path to database  YAML file to read")

def lemmings_clean(database):
    """
    Clean lemmings run files in current folder
    """
    import os
    import sys
    import shutil
    from lemmings_hpc.chain.database import Database
    from lemmings_hpc.cli_helper import remove_files_folders, gather_default_files_folders_to_clean  
    # need to add option to have other database.yml name to look at
    # cfr. lemmings status of FEATURE/parallel branch

    try:
        lst_remove = gather_default_files_folders_to_clean(database)
    except FileNotFoundError as excep:
        print("Error: ", excep)
        return
    except KeyError as excep:
        print(excep)
        if 'use lemmings-farming clean' in str(excep):
            return

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
main = click.CommandCollection(sources=[cli], help="This is the help of lemmings")

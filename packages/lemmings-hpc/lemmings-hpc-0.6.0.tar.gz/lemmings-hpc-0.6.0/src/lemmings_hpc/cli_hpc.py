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
@click.option("--parallel", '-p', is_flag=True,
              help="Parallel mode activation, Expert users only")
@click.option("--noverif", is_flag=True)
@click.option("--restart", is_flag=True,
              help="If activated, the last chain will be continued.")
@click.option('--job-prefix', required=False, type=str, default = None,
    help = "Job prefix to be used in chain name. Will be prioritised over the {workflow}.yml file")
@click.option('--user-machine', required=False, type=str, default = None,
    help = "Allows user specification of  path to {machine}.yml file")

def lemmings_cli(workflow, status, yaml, noverif, restart, parallel, job_prefix, user_machine):
    """
        Depreciation Warning!!! Favor the use of 'lemmings' or 'lemmings-farming'.
        This is the command to launch your workflow with Lemmings.
        ' lemmings-hpc run {workflow_name} '
    """

    import subprocess
    import warnings
    if parallel:
        # should be a way to call the other 
        # import lemmings_hpc.cli_farming-> due to decorator tricky and not advised
        # use subprocess instead
        warnings.warn("DepreciationWarning: Use 'lemmings-farming run {workflow}' in the future.")
        subprocess.call('lemmings-farming run '+ workflow,shell=True)
        return
    
    warnings.warn("DepreciationWarning: Use 'lemmings run {workflow}' in the future.")
    option_list = [workflow, '--status='+status]
    if yaml is not None:
        option_list.append('--yaml='+yaml)
    if job_prefix is not None:
        option_list.append('--job-prefix='+job_prefix)
    if user_machine is not None:
        option_list.append('--user-machine='+user_machine)
    if restart:
        option_list.append('--restart')
    if noverif:
        option_list.append('--noverif')
    command = 'lemmings run '+ ' '.join(option_list)
    subprocess.call(command,shell=True)
    return

    #-----Depreciated-----------------------#
    #---------------------------------------#
    #---------------------------------------#
    #---------------------------------------#
    #pylint: disable=too-many-function-args

    #get path of the WorkFlow desired
    if workflow.lower().endswith(('.yml', '.py')):
        raise ValueError("A workflow name can't contain an extension like '.yml', "
                         + "please enter a valid workflow name. ")

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
                          user_machine = user_machine)

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
    if user_machine is not None:
        database.update_current_loop("user_machine",os.path.abspath(user_machine))

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

    if parallel:
        try:
            lemmings.create_replicate_workflows()
        except LemmingsStop as stop:
            _handle_exception(lemmings.lemmings_job,lemmings.database,
                            stop, lemmings_stop= True)
            print(stop)
            sys.exit()

    lemmings.run()

@cli.command('kill')
def lemmings_kill():
    """ 
        Depreciation Warning!!! Favor the use of 'lemmings' or 'lemmings-farming'.
        Kill the current job and pjob of lemmings

        In farming mode, if command called from the main directory
        all running Workflows will be killed.
    """
    import warnings
    import os
    import yaml
    from lemmings_hpc.chain.database import Database
    import subprocess as sbp

    warnings.warn("DepreciationWarning: Use 'lemmings kill' or 'lemmings-farming kill' in the future.")

    parallel_kill = False

    database = Database()

    env_var = dict(os.environ)
    try: # need to know how to kill jobs
        machine_path = env_var["LEMMINGS_MACHINE"]
    except KeyError:
        print("No LEMMINGS_MACHINE environment variable specified")
        return

    try: # check if parallel mode
        par_dict, = database.get_current_loop_val('parallel_runs')
        kill_confirm = input("Are you sure you want to kill all lemmings Workflows? (yes/no)  ")
        if kill_confirm != 'yes':
            return
        parallel_kill = True
    except KeyError:
        pass

    with open(machine_path) as fin:
        machine_dict = yaml.load(fin, Loader=yaml.SafeLoader)

    def kill_chain(database):
        try:
            job_id = database.get_loop_val('job_id', 0) #latest loop
            pjob_id = database.get_loop_val('pjob_id', 0)
        except KeyError:
            print("No job and / or post job to kill in current database loop")
            return

        print("Killing the current job and post-job...")

        try:
            #print(type(machine_dict['commands']['cancel']))
            machine_dict['commands']['cancel']
        except KeyError:
            print("No 'cancel' command specified in the machine file")
            return

        sbp.run([machine_dict['commands']['cancel'],
                job_id],
                stdout=sbp.PIPE)
        print("   job  "+ str(job_id) + " was killed")
        sbp.run([machine_dict['commands']['cancel'],
                pjob_id],
                stdout=sbp.PIPE)
        print("   pjob "+ str(pjob_id) + " was killed")

    if parallel_kill:
        # we have to do two things:
        #   1) update status from jobs that were waiting to killed "K"
        #   2) kill the jobs that are running

        # check first if there is anything chain to kill
        workflows_to_kill = [key for key, val in par_dict.items() if val == 'start']
        if not workflows_to_kill: 
            print("No workflows to kill")
            return

        par_dict = dict([(key,val) if val != 'wait' else (key, 'kill')
                            for key, val in par_dict.items() ])
        database.update_current_loop('parallel_runs',[par_dict])

        main_dir = os.getcwd()
        for wf_dir in workflows_to_kill:
            os.chdir(wf_dir)
            kill_chain(database)
            os.chdir(main_dir)

        # now we'll update the database as we successfully killed the active chains
        par_dict = dict([(key,val) if val != 'start' else (key, 'kill')
                            for key, val in par_dict.items() ])
        database.update_current_loop('parallel_runs',[par_dict])
        return

    # for non farming case
    kill_chain(database)






@cli.command('safestop')
def lemmings_safestop():
    """
    Lemmings finish properly the current loop and stop.
    """
    from lemmings_hpc.chain.database import Database
    
    database = Database()
    database.update_loop('safe_stop', True, 0) #latest


@cli.command('endlog')
# @click.option("--job", "-j", type=str, default=None,
#               help="The job name you want to show")
def lemmings_endlog():
    """
    Show the lemmings log of the actual/most_recent job upon finishing.
    """
    import os
    from lemmings_hpc.chain.database import Database
    db = Database()
    # database = db._database
    chain_name = db.latest_chain_name
    if chain_name is None:
        print("No lemmings database found. Check your current directory...")
    else:
        with open(os.path.join(chain_name, chain_name + ".log"), 'r') as fin:
            print(fin.read())

@cli.command('status')
# @click.option("--timeformat", "-tf", required=False , type=click.Choice(['s','ms']), default= 'ms',
#               help="Simulation time format")
@click.option("--database", "-db", required=False , type=str, default = None,
              help="Path to database  YAML file to read")
@click.option("--progress", '-p', is_flag=True,
              help="If activated, the latest progress will also be shown.")
# @click.option("--job", "-j", type=str, default=None,
#               help="The job name you want to show")
def lemmings_status(database, progress):
    """
    Depreciation Warning!!! Favor the use of 'lemmings' or 'lemmings-farming'.
    Show the status during runtime
    """
    import warnings
    from lemmings_hpc.chain.database import Database

    warnings.warn("DepreciationWarning: Use 'lemmings status' or 'lemmings-farming status' in the future.")

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

    try:
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
    Depreciation Warning!!! Favor the use of 'lemmings' or 'lemmings-farming'.
    Clean lemmings run files in current folder
    """
    import os
    import warnings
    import sys
    import shutil
    from lemmings_hpc.chain.database import Database

    warnings.warn("DepreciationWarning: Use 'lemmings clean' or" + 
                    " 'lemmings-farming clean' in the future.")

    # need to add option to have other database.yml name to look at
    # cfr. lemmings status of FEATURE/parallel branch

    lst_remove = ["__pycache__", "batch_job", "batch_pjob", "database.yml"]

    def remove(my_path):
        """
        Clean removal of file/folders based on the database.yml file info
        """
        if os.path.exists(my_path):
            if os.path.isfile(my_path):
                print("> Remove file: %s" % my_path)
                os.remove(my_path)
                return

            if os.path.isdir(my_path):
                print("> Remove folder: %s" % my_path)
                shutil.rmtree(my_path)
                return

    try:
        if database is not None:
            if not os.path.isfile(database):
                raise FileNotFoundError(database + " does not exist")
            lst_remove = [string.replace('database.yml',database) for string in lst_remove]
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

    try:
        db.latest_chain_name
    except UnboundLocalError as excep:
        print("'lemmings clean' aborted")
        return
    except TypeError as excep:
        print("'lemmings clean' aborted")
        return 2

    # Todo: add later option to remove only latest chain name
    try:
        chain_names = db.get_chain_names()
    except TypeError as excep:
        print("ValueError:", excep)
        print("Your file database.yml is corrupted, I can't automatically clean this folder\n")
        sys.exit()

    lst_remove.extend(chain_names)

    # currently only remove WF_xxx folders associated with latest chain
    try:
        par_dict, = db.get_current_loop_val('parallel_runs')
        lst_remove.extend(list(par_dict))
    except KeyError:
        pass

    for path in lst_remove:
        remove(path)


@cli.command('info')
@click.option("--queues", "-q", is_flag=True,
              help="Get {machine}.yml queues info")

def lemmings_info(queues):
    import os
    import yaml
    if queues:
        env_var = dict(os.environ)
        try:
            machine_path = env_var["LEMMINGS_MACHINE"]
        except KeyError:
            print("No LEMMINGS_MACHINE environment variable specified")
            return

        print("Path to {machine}.yml file", machine_path)
        with open(machine_path) as yaml_in:
            tmp = yaml.load(yaml_in, Loader=yaml.FullLoader)
            print("Queues available in {machine}.yml file:")
            for line in tmp['queues']:
                print("\t"+line)
#Main function called by setup.py
main = click.CommandCollection(sources=[cli], help="This is the help of lemmings-hpc")

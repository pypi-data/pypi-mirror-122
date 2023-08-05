"""Module helper for the CLI of lemmings"""
import os
import random
import string
import glob
from pathlib import Path
from pkg_resources import resource_filename
from lemmings_hpc.chain.path_tool import PathTools

# We have to avoid offensive names, here in french
FORBIDDEN_NAMES = [
    "", "PUTE", "PEDE", "BITE", "CACA", "ZIZI", "CUCU", "PIPI", "CONE",
    "CULE", "PENE", "SODO", "SUCE", "SUCA", "KUKU", "CUNI"]

def custom_name():
    """
    Random Name generator --> Cons + Vowels + Cons + Vowels + 2*Int
    """
    vowels = list("AEIOU")
    consonants = list(set(string.ascii_uppercase) - set(vowels))
    name = ""
    while name in FORBIDDEN_NAMES:
        name = ""
        name += random.choice(consonants)
        name += random.choice(vowels)
        name += random.choice(consonants)
        name += random.choice(vowels)

    name += str(random.randrange(1, 10))
    name += str(random.randrange(1, 10))
    return name


def get_workflow_py(workflow):
    """
    *Get the path of the {workflow}.py file.*

    :param workflow: workflow name
    :type workflow: str
    """
    path_tool = PathTools()
    env_var = dict(os.environ)
    catch = False

    if Path("./" + workflow + ".py").is_file():
        wf_py_path = path_tool.abspath(workflow + ".py")
        catch = True
    if catch is False and "LEMMINGS_WORKFLOWS" in env_var:
        wf_py_path = env_var["LEMMINGS_WORKFLOWS"]
        if Path(wf_py_path).is_file():
            catch = True
        else:
            raise EnvironmentError("\n ENVIRONMENT VAR :\nunable to open file at " + wf_py_path)
    
    # Deactivate for now (JJH 1/9/2021)
    if catch is False:
        wf_py_path = None
    #     wf_py_path = Path(resource_filename('lemmings_hpc', "")) / "chain" / "workflows" /  str(workflow + ".py") #pylint: disable=line-too-long
    #     if Path(wf_py_path).is_file():
    #         catch = True
    #     else:
    #         raise EnvironmentError("\nFOLDER LEMMING : unable to open file at " + str(wf_py_path))

    if wf_py_path is not None:
        return wf_py_path

    raise EnvironmentError("Your specified workflow '" + workflow + "'doesn't exist in :\n"
                           + "  - current directory\n"
                           + "  - Environment variable ('LEMMING_WORKFLOWS')\n")
                           #+ "  - Folder workflows of lemmings\n")


def get_workflow_yml(workflow, user_yaml = False):
    """
    *Get the path of the {workflow}.yml file.*

    :param workflow: workflow name
    :type workflow: str
    """
    path_tool = PathTools()
    if user_yaml:
        if Path(workflow + ".yml").is_file():
            wf_yml_path = path_tool.abspath(workflow + ".yml")
        else:
            raise FileNotFoundError("Oops!  Couldn't find the %s.yml file relative to your current directory. Please generate it." % workflow)
    else:
        if Path("./" + workflow + ".yml").is_file():
            wf_yml_path = path_tool.abspath(workflow + ".yml")
        else:
            raise FileNotFoundError("Oops!  Couldn't find the %s.yml file in your current directory. Please generate it." % workflow)

    return wf_yml_path


def check_cpu_input(cpu_limit):
    """
    *Ask a confirmation of the cpu_limit to the user*

    :param cpu_limit: the cpu limit found in the {workflow}.yml file
    :type cpu_limit: float
    """
    cpu_confirm = input("Your CPU limit is " + str(cpu_limit) + " [hours]."
                        + " Confirm it typing the same value: ")

    if int(cpu_confirm) != int(cpu_limit):
        raise ValueError("Confirmation failed: " + str(cpu_confirm) + " != " + str(cpu_limit))


def find_all_wf():
    """
    *Find all available workflows.*
    They can be in the current directory,
    workflows folder of lemmings or in a environment variable.
    """
    path_workflows = {"current": {},
                      "env_var": {},
                      "lemmings": {}}

    files_wf = []
    env_var = dict(os.environ)

    #find in the workflows folder of lemmings
    path_folder_wf = Path(resource_filename('lemmings_hpc', "")) / "chain" / "workflows"
    for file in glob.glob(str(path_folder_wf) + "/*.py"):
        if "__init__" not in file:
            files_wf.append(file.split("/")[-1])
            path_workflows["lemmings"][files_wf[-1].split('.py')[0]] = file

    #find in current directory 
    for file in glob.glob("*.py"):
        if file in files_wf: # -> requires to be def
            path_workflows["current"][file.split('/')[-1].split('.py')[0]] = file

    #find in environment variable
    if "LEMMINGS_WORKFLOWS" in env_var:
        for var in env_var["LEMMINGS_"]:
            if var.split('/')[-1] in files_wf:
                path_workflows["env_var"][var.split('/')[-1].split('.py')[0]] = var

    return path_workflows


def kill_chain(database, machine_dict):
    """ Function running subprocess to kill an active job and post job

        Input:
            :database: Database object
            :machine_dict: dict, containing commands to enable killing of jobs

        Output:
            :None
    """

    import subprocess as sbp
    try:
        job_id = database.get_loop_val('job_id', 0) #latest loop
        pjob_id = database.get_loop_val('pjob_id', 0)
    except KeyError:
        print("No job and / or post job to kill in current database loop")
        return
    print("Killing the current job and post-job...")

    try:
        assert isinstance(machine_dict, dict)
    except AssertionError:
        print("Provided machine dictionary is not a dictionary")
        return

    try:
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

def remove_files_folders(my_path):
    """
        Clean removal of file/folders based on the database.yml file info
    """
    import os
    import shutil
    if os.path.exists(my_path):
        if os.path.isfile(my_path):
            print("> Remove file: %s" % my_path)
            os.remove(my_path)
            return

        if os.path.isdir(my_path):
            print("> Remove folder: %s" % my_path)
            shutil.rmtree(my_path)
            return

def gather_default_files_folders_to_clean(database, farming = False):
    """ Standard lemmings files to remove by the clean function

        Input:
            :database: Database object of lemmings

        Output:
            :lst_remove: list of string, contains files and folders to remove
    """

    from lemmings_hpc.chain.database import Database

    lst_remove = ["__pycache__", "batch_job", "batch_pjob", "database.yml", "used_machine.yml"]

    if database is not None:
        if not os.path.isfile(database):
            raise FileNotFoundError(database + " does not exist")
        lst_remove = [string.replace('database.yml',database) for string in lst_remove]
    else:
        if not os.path.isfile("database.yml"):
            raise FileNotFoundError("database.yml does not exist")

    if database is not None:
        db = Database(database)
    else:
        ## this init will generate a database.yml file,
        ## so if not present we should check before
        db = Database()

    # First check that we are in the correct directory to launch this command
    try:
        par_dict, = db.get_current_loop_val('parallel_runs')
        if not farming:
            print("ERROR: you're in farming main directory")
            print("       Use 'lemmings-farming clean' instead")
            raise KeyError('use lemmings-farming clean')
    except KeyError as excep:
        if 'use lemmings-farming clean' in str(excep):
            raise KeyError('use lemmings-farming clean')
        if farming:
            print("ERROR: you're not in farming main directory")
            print("       Use 'lemmings clean' instead")
            raise KeyError('use lemmings clean')

    try: # perhaps redundant as  db.get_current_loop_val will already
         # try access latest chain name
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
        return

    lst_remove.extend(chain_names)
    if farming:
        return (lst_remove, db)
    return lst_remove


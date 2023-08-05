"""
The machine class that contains user parameter
+ machine cmd
+ machine template.
"""
import os
import sys
import subprocess as sbp
from collections import namedtuple
from datetime import datetime#, timedelta

import yaml

from lemmings_hpc.chain.path_tool import PathTools

#__all__ = ["Machine"]

def convert(dictionary):
    """
    *Convert a dict( ) to a NamedTuple( ).*
    """
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)

def get_user_params(path):
    """
    Get the user parameters and generate a NamedTuple with it
    """
    with open(path, 'r') as fin:
        tmp = yaml.load(fin, Loader=yaml.FullLoader)
    # check if file is empty (or everything commented)
    if tmp is None:
        raise ValueError("Oops!  The provided YAML file %s is empty" %path)
    return convert(tmp)

def template_parser(user_tuple, queue_template, job_name, pjob_name):
    """
    Machine template parser that remplace some keys by the user parameters
    """
    lines = queue_template["header"].split("\n")
    content = ""
    for line in lines:
        if "-LEMMING-JOB_NAME-" in line:
            line = line.replace("-LEMMING-JOB_NAME-",
                                job_name)
        if "-LEMMING-POSTJOB_NAME-" in line:
            line = line.replace("-LEMMING-POSTJOB_NAME-",
                                pjob_name)
        if "-LEMMING-WALL-TIME-" in line:
            line = line.replace("-LEMMING-WALL-TIME-",
                                str(queue_template["wall_time"]))
        if "-EXEC-" in line:
            line = line.replace("-EXEC-",
                                user_tuple.exec)
        if "-EXEC_PJ-" in line:
            line = line.replace("-EXEC_PJ-",
                                user_tuple.exec_pj)

        content += line + '\n'
    return content


def get_machine_template(user_tuple, path_machine, job_name, pjob_name,
                            commands_only = False):
    #pylint: disable=line-too-long
    """
    Get the machine template + cmd and generate a NamedTuple with it

    TODO: split in functions to get job, pjob, visu? and commands
    """

    with open(path_machine) as fin:
        tmp = yaml.load(fin, Loader=yaml.FullLoader)

    # add the batch key, with substitutions

    cmd = convert(tmp["commands"])
    if commands_only:
        return cmd

    # Needed to add this check to enable usage when only job or pjob of interest
    # NOTE: this function and template_parser() are too thightly coupled with job/pjob
    job_template = None
    if job_name is not None:
        if pjob_name is None:
            pjob_name = "None"
        tmp["queues"][user_tuple.job_queue]["batch"] = template_parser(user_tuple,
                                                                   tmp["queues"][user_tuple.job_queue],
                                                                   job_name,
                                                                   pjob_name)
        job_template = convert(tmp["queues"][user_tuple.job_queue])
        if pjob_name == "None": # revert previously made change
            pjob_name = None

    pj_template = None
    if pjob_name is not None:
        if job_name is None:
            job_name = "None"
        tmp["queues"][user_tuple.pjob_queue]["batch"] = template_parser(user_tuple,
                                                                    tmp["queues"][user_tuple.pjob_queue],
                                                                    job_name,
                                                                    pjob_name)

        pj_template = convert(tmp["queues"][user_tuple.pjob_queue])
        if job_name == "None": # revert previously made change
            job_name = None

    try:
        tmp["queues"][user_tuple.visu_queue]["batch"] = template_parser(user_tuple,
                                                                        tmp["queues"][user_tuple.pjob_queue],
                                                                        job_name,
                                                                        pjob_name)
        visu_template = convert(tmp["queues"][user_tuple.visu_queue])
    except:
        visu_template = None

    return cmd, job_template, pj_template, visu_template

class Machine(PathTools):
    """
    Machine class of Lemmings
    """
    def __init__(self,
                 path_yml,
                 chain_name,
                 user_machine = None,
                 base_dir=None,
                 local_machine_copy = False,
                 debug = False):
        """
        :param path_yml: path to the user parameters file {workflow}.yml
        :type path_yml: str
        :param job_name: The name of the current Lemmings job
        :type job_name: str
        :param base_dir: the base directory to initialise the PathTools class.
        :type base_dir: str
        """
        env_var = dict(os.environ)
        PathTools.__init__(self, base_dir)

        self.path_yml = path_yml
        self.job_name = chain_name
        self.pjob_name = chain_name + "_pj"
        self.custom_machine = False # parameter for the farming mode

        try:
            if not self.user.job_prefix in ['None','none']:
                self.job_name = self.user.job_prefix + "_" + self.job_name
                self.pjob_name = self.user.job_prefix + "_" + self.pjob_name
        except:
            pass

        # A base situation with $LEMMINGS_MACHINE
        try:
            self.path_machine = env_var["LEMMINGS_MACHINE"]
        except KeyError:
            if not debug: # debug key used for pytest
                raise EnvironmentError("There is no 'LEMMINGS_MACHINE' variable in your Environment"
                                   + " (export LEMMINGS_MACHINE=path/...)")

        # A situation override
        if user_machine is not None:
            if user_machine == 'farming_custom_machine':
                self.custom_machine = True
                print("A customized {machine}.yml file will be used in this farming mode")
            else:
                self.path_machine = user_machine
                print('Overriding the $LEMMINGS_MACHINE by a user defined {machine}.yml')

        self.check_correct_machine_inputs()

        if local_machine_copy:
            dict_info_job = {'wall_time', 'header','core_nb'}
            dict_info_pj = {'wall_time', 'header'}
            local_machine = {'commands':dict(self.cmd._asdict()),
                            'queues':{self.user.job_queue:
                                dict([(key,self.job_template._asdict()[key]) for key in dict_info_job]),
                                self.user.pjob_queue:
                                dict([(key,self.pj_template._asdict()[key]) for key in dict_info_pj]),
                                }
                            }

            with open('used_machine.yml', 'w') as yamlout:
                yaml.dump(local_machine, yamlout)

            self.path_machine = 'used_machine.yml'
        # in farming mode, we would create it in local folder and should then be copied


    @property
    def user(self):
        """
        *Get the user parameters from {workflow}.yml
        """
        return get_user_params(self.abspath(self.path_yml))

    @property
    def cmd(self):
        """
        *Get the machine commands {machine}.yml
        """
        return get_machine_template(self.user,
                                    self.abspath(self.path_machine),
                                    self.job_name,
                                    self.pjob_name)[0]
    @property
    def job_template(self):
        """
        *Get the job template from {machine}.yml
        """
        return get_machine_template(self.user,
                                    self.abspath(self.path_machine),
                                    self.job_name,
                                    self.pjob_name)[1]
    @property
    def pj_template(self):
        """
        *Get the post-job template from {machine}.yml
        """
        return get_machine_template(self.user,
                                    self.abspath(self.path_machine),
                                    self.job_name,
                                    self.pjob_name)[2]

    @property
    def visu_template(self):
        """
        *Get the post-job template from {machine}.yml
        """
        return get_machine_template(self.user,
                                    self.abspath(self.path_machine),
                                    self.job_name,
                                    self.pjob_name)[3]

    def check_correct_machine_inputs(self):
        """ We will check if the core_nb has been specified in the machine.yml file.

            TODO: should go further than this -> a SCHEMA?
        """
        # core_nb = self.job_template.core_nb
        if self.custom_machine:
            # We do not do any check as the machine file still has to be created
            return

        try:
             core_nb = self.job_template.core_nb
        except AttributeError as excep:
            if "'GenericDict' object has no attribute 'job_queue'" in str(excep):
                raise KeyError("Your specified queue can't be found."+
                        "Check your {workflow}.yml and {machine}.yml")
            else:
                raise KeyError("Parameter core_nb not found in machine.yml file, please specify it:"
                            + " core_nb = (number of nodes) x (number of processes per node) ."
                        )

    def submit(self,
               batch_name,
               dependency=None,
               submit_path=None):
        """
        Submit a job on a NFS machine.

        :param batch_name: Name of the batch
        :type batch_name: str
        :param dependency: Job ID of the job to be depend with.
        :type dependency: int
        """

        # check if batch exists
        if not os.path.isfile(os.path.join(submit_path,batch_name)):
            raise FileNotFoundError('Batch file not found. Did you activate user_batch in expert_params?')

        if dependency is None:
            out = sbp.run([self.cmd.submit,
                           batch_name],
                          stdout=sbp.PIPE,
                          stderr=sbp.STDOUT,
                          cwd=submit_path)
        else:
            out = sbp.run([self.cmd.submit,
                           self.cmd.dependency + str(dependency),
                           batch_name],
                          stdout=sbp.PIPE,
                          stderr=sbp.STDOUT,
                          cwd=submit_path)

        out = out.stdout
        job_id = out.decode('utf-8')[:-1].split(" ")[-1]
        return job_id

    def cancel(self,
               job_id):
        """
        Cancel a job on a NFS machine.
        """
        sbp.run([self.cmd.cancel,
                 job_id],
                stdout=sbp.PIPE)

    def get_cpu_cost(self, job_id):
        """
        *Get the CPU cost of the previous Run.*

        :param job_id: Job ID of the previous run
        :type job_id: int
        """
        command_cpu = self.cmd.get_cpu_time.replace("-LEMMING-JOBID-", str(job_id))

        core_nb = 1 # Dangerous, consider something else,
                    # and add a check in machine file before

        try:
             core_nb = self.job_template.core_nb
        except AttributeError:
            pass

        out = sbp.run(command_cpu,
                    shell=True,
                    stdout=sbp.PIPE)
        out = out.stdout
        out = out.decode('utf-8')[:-1].strip().split(" ")[0]
        out_day = 0
        try_sec = False
        if '-' in out: # we have a format with day as D-H:M:S
            out_day = out.split('-')[0]
            out = out.split('-')[1:][0]
        try:
            out = datetime.strptime(out, '%H:%M:%S').time()
        except ValueError:
            try:
                out = datetime.strptime(out, '%M:%S').time()
            except ValueError:
                try_sec = True


        if not try_sec:
            out_sec = (float(out_day) * 24 * 3600
                    +  out.hour * 3600                             #in seconds
                    + out.minute * 60
                    + out.second)
        else:
            try:
                out_sec = float(out)
            except ValueError as excep:
                print("Error, unknown scheduler CPU format. Job stopped due to infinite loop danger. ", excep)
                sys.exit()

        return (core_nb * out_sec)/3600

        # NEED TO HANDLE:
            # 1-00:00:00
            # 00:30:00    hours min seconds
            # 7-01:00:00    day hours min seconds
            # 3:34    min and seconds
            # 3600     seconds

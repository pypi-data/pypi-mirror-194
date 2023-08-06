#!/usr/bin/env python
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import print_function
from BlackDynamite import *
import os
import stat
import subprocess
import re
import socket


admissible_params = {"walltime": str,
                     "email": str,
                     "nodes": int,
                     "module": [str],
                     "cpus-per-task": int,
                     "cpus-per-node": int,
                     "cwd": bool,
                     "slurm_option": str,
                     "option_delimeter": str}

default_params = {"walltime": "48:00:00",
                  "cwd": True,
                  "nodes": 1,
                  "cpus-per-task": 1,
                  "option_delimeter": ","}

help = {"walltime": "Specify the wall time for the runs",
        "email": "Specify the email to notify",
        "nodes": "Number of nodes for the job",
        "slurm_option": "Allow to provide additional SLURM options",
        "option_delimeter": "Delimeter string for additional options",
        "module": "List of modules to load",
        "cpus-per-node": "Number of CPU per nodes",
        "cpus-per-task": "Number of thread per MPI process",
        "cwd": "Run by default in the run folder"}

mandatory = {"cpus-per-node": True}


def launch(run, params):

    _exec = run.getExecFile()
    head = "#!/bin/bash\n\n"

    head += "#SBATCH --time={0}\n".format(params["walltime"])

    if ("email" in params):
        head += "#SBATCH --mail-type=ALL\n"
        head += "#SBATCH --mail-user={0}\n".format(params["email"])

    slurm_head_name = "#SBATCH --job-name={0}_{1}\n".format(
        run["run_name"], run.id)
    head += slurm_head_name

    run["state"] = "SLURM submit"
    if ("nproc" in params):
        run["nproc"] = params["nproc"]

    nproc = run["nproc"]
    try:
        nodes = max(nproc * params["cpus-per-task"] //
                    params["cpus-per-node"], 1)
    except Exception as e:
        print(params.keys())
        print(e)
        raise e

    head += "#SBATCH --nodes={0}\n".format(nodes)
    head += "#SBATCH --ntasks={0}\n".format(nproc)
    head += "#SBATCH --cpus-per-task={0}\n".format(params["cpus-per-task"])

    if "slurm_option" in params:
        for option in params["slurm_option"].split(params["option_delimeter"]):
            # To get consistent behavior between --slurm_option=""
            # and --slurm_option ""
            m = re.match(r'^--(\S+)$', option)
            if m:
                option = m.group(1)
            head += "#SBATCH --{}\n".format(option)

    if (params["cwd"]):
        head += "#SBATCH --chdir=__BLACKDYNAMITE__run_path__\n"

    if ("module" in params):
        head += "\nmodule purge\n"
        for i in params["module"]:
            head += "module load {0}\n".format(i)

    run.update()

    head += """

export BLACKDYNAMITE_HOST=__BLACKDYNAMITE__dbhost__
export BLACKDYNAMITE_SCHEMA=__BLACKDYNAMITE__study__
export BLACKDYNAMITE_STUDY=__BLACKDYNAMITE__study__
export BLACKDYNAMITE_RUN_ID=__BLACKDYNAMITE__run_id__
export BLACKDYNAMITE_USER=""" + params["user"] + """

on_kill()
{
updateRuns.py --updates \"state = SLURM killed\" --truerun
exit 0
}

on_stop()
{
updateRuns.py --updates \"state = SLURM stopped\" --truerun
exit 0
}

# Execute function on_die() receiving TERM signal
#
trap on_stop SIGUSR1
trap on_stop SIGTERM
trap on_kill SIGUSR2
trap on_kill SIGKILL
"""

    _exec["file"] = run.replaceBlackDynamiteVariables(head) + _exec["file"]

    f = open(_exec["filename"], 'w')
    f.write(_exec["file"])
    f.close()
    # os.chmod(_exec["filename"], stat.S_IRWXU)
    print("execute sbatch ./" + _exec["filename"])
    print("in dir ")
    subprocess.call("pwd")
    if params["truerun"] is True:
        ret = subprocess.call("sbatch " + _exec["filename"], shell=True)

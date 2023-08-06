import datetime
import importlib
import logging
import json
import os
import socket
import sys
import traceback

import click
import yaml

from pype import utils


logging.basicConfig(level=logging.INFO)


class Status:
    def __init__(self, dir_):
        self.dir = dir_
        self.status = "status"
        for status in ["Done", "Failed", "Running"]:
            if os.path.exists(os.path.join(dir_, status)):
                self.status = status

        self.status_path = os.path.join(dir_, self.status)

        with open(self.status_path, "w") as f:
            f.write("Host: " + socket.gethostname() + "\n")

    def done(self):
        self._set_status("Done")

    def running(self):
        self._set_status("Running")

    def failed(self):
        self._set_status("Failed")

    def _set_status(self, status):
        timestamp = datetime.datetime.now().strftime("%y/%m/%d-%H:%M:%S")

        with open(self.status_path, "a") as status_file:
            status_file.write(status + ": " + timestamp + "\n")

        status_path = os.path.join(self.dir, status)
        os.rename(self.status_path, status_path)

        self.status = status
        self.status_path = status_path


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--log",
    "-l",
    default=False,
    is_flag=True,
    help="will log stdout and stderr to a file log.txt instead of stdout, useful when using "
    "screen for example",
)
@click.argument("config_file")
def run(config_file, log):
    if _uncomitted():
        if permission_to_continue("You have uncomitted changes."):
            logging.info("Job aborted.")
            sys.exit()

    config = yaml.load(open(config_file, "r"), Loader=yaml.FullLoader)

    if isinstance(config, list):
        for config_ in config:
            _run(config_, log, skip_done=True)

    else:
        _run(config, log, skip_done=False)


def _run(config, log, skip_done):

    job_dir = config["job_dir"]

    status = Status(job_dir)

    if status.status == "Running" or status.status == "Done":
        if skip_done:
            print(f"Skipping {config['job_id']} ... " )
            return

        if permission_to_continue(f"Job is {status.status}."):
            print("job aborted")
            sys.exit()

    print_running_job(config["job_id"])

    utils.save_git_sha(job_dir)

    status.running()

    if log:
        sys.stdout = open(os.path.join(job_dir, "stdout.log"), "w")
        sys.stderr = open(os.path.join(job_dir, "stderr.log"), "w")

    try:
        module = _import_module(config["script_path"])
        if not hasattr(module, "main"):
            raise RuntimeError(f"{config['script_path']} has no main function.")

        module.main(config)
        status.done()

    except Exception:  # pylint: disable=broad-except
        status.failed()
        print(traceback.format_exc())


def print_running_job(job_id):
    msg = f"Running job {job_id}"
    hashs = (4 + len(msg)) * "#"
    ws = "      "

    print(f"{ws+hashs}\n{ws+'  '+msg}\n{ws+hashs}\n")


@cli.command()
@click.option(
    "--log",
    "-l",
    default=False,
    is_flag=True,
    help="will log stdout and stderr to a file log.txt instead of stdout, useful when using "
    "screen for example",
)
@click.option(
    "--force_run",
    "-f",
    default=False,
    is_flag=True,
    help="will log stdout and stderr to a file log.txt instead of stdout, useful when using "
    "screen for example",
)
@click.argument("job_configs")
def run_pipeline(job_configs, log, force_run):
    if _uncomitted():
        if permission_to_continue("You have uncomitted changes."):
            logging.info("Job aborted.")
            sys.exit()


    dir_ = os.path.dirname(job_configs)
    job_configs = json.load(open(job_configs))

    for job_config in job_configs:
        full_path = os.path.join(dir_, job_config)

        _run(full_path, log, force_run)


def permission_to_continue(msg):
    return input(msg + "Type 'y' or 'yes' to continue anyways\n").lower() not in [
        "y",
        "yes",
    ]


def _import_module(path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def _uncomitted():
    if not utils.GIT_CONTROL:
        return False

    cmd = r"git status | grep -q '\smodified:\s'"
    code = os.system(cmd)
    return code == 0

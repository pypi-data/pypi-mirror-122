
from pype.baseconfig import BaseConfig


class Config(BaseConfig):
    script_path = "example/failing_job.py"

def main(config):
    _ = config
    print('hello')
    1/0

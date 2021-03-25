import subprocess


def run(command, stderr=None):
    return subprocess.check_output(command, shell=True, stderr=stderr, universal_newlines=True)

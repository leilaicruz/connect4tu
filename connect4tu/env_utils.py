
import os
import subprocess

def load_env_from_script(script_path):
    """
    Loads environment variables from a shell script into the current Python process.
    """
    command = ['bash', '-c', f'source {script_path} && env']
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.decode("utf-8").partition("=")
        os.environ[key.strip()] = value.strip()
    proc.communicate()

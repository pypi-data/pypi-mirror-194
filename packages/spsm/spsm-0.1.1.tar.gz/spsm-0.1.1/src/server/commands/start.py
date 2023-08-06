import os
import subprocess
from server.enums.log_levels import LogLevels

def run(wrapper, *args):
  if wrapper.is_running():
    wrapper.log_handler.append('Server already running', severity=LogLevels.WARN)
    return

  wrapper.log_handler.append('Starting Server now!!')

  start_command = f"{str(wrapper.config['start_command']).replace('(jar_name)', wrapper.config['jar_name'])}"
  wrapper.server_process = subprocess.Popen(start_command,
                                            shell=True,
                                            stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True)

def help(wrapper):
  wrapper.append_log("Starts the server using config['start_command'] in config['server_directory]")

def summary():
  return "Starts the server"
import subprocess

def run(wrapper, *args):
  wrapper.reload_config()

  

def help(wrapper):
  wrapper.append_log("Reloads the config settings into the environment")

def summary():
  return "Reload config"
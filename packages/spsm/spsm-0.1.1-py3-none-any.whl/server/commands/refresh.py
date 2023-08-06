import subprocess

def run(wrapper, *args):
  wrapper.append_log("Refreshing!!")
  wrapper.screen_handler.refresh()

  

def help(wrapper):
  wrapper.append_log("This command will refresh the input and output windows")

def summary():
  return "refresh screen"
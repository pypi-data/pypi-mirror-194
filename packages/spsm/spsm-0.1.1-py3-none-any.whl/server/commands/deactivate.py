def run(wrapper, *args):
  wrapper.deactivate()

def help(wrapper):
  wrapper.append_log("Deactivate Server")

def summary():
  return "Deactivates server"
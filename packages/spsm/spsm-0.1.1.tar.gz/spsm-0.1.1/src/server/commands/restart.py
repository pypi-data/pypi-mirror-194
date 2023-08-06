def run(wrapper):
  wrapper.input_handler.handle_command('stop')
  wrapper.input_handler.handle_command('start')

def help(wrapper):
  wrapper.append_log("Restarts the server")

def summary():
  return "Restarts the server"

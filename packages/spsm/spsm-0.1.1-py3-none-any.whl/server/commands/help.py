def run(wrapper, *args):
  if len(args) == 0:
    wrapper.list_commands()
    return
  command = args[0]
  
  if command and command in wrapper.input_handler.command_modules.keys() and hasattr(wrapper.input_handler.command_modules[command], 'help'):
    wrapper.append_log(f"---- {command.upper()} ----")
    wrapper.input_handler.command_modules[command].help(wrapper)
    wrapper.append_log(f"-----{'-'*len(command)}-----")
  else:
    wrapper.append_log(f"Command '{command}' not found.", severity=2)

def help(wrapper):
  wrapper.append_log("Can be passed another command as an argument to receive more information.")

def summary():
  return "Provides info about commands"
import subprocess

def run(wrapper, *args):
  screen_name = wrapper.config['screen_name']
  wrapper.screen_handler.clear_input_window()
  wrapper.prepare_for_detach()
  subprocess.run(['screen', '-d', screen_name])

  

def help(wrapper):
  wrapper.append_log("Use this command to detach from the server console without deactivating it. This can also be done by pressing 'Ctrl+A' then 'Ctrl+D")

def summary():
  return "Detach from console."
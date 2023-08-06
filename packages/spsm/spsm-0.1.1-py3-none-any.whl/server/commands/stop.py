import time

from server.enums.log_levels import LogLevels

def run(wrapper):
  if not wrapper.is_running():
    wrapper.append_log("Server is not running.", severity=LogLevels.ALERT)
    return

  delay = wrapper.config['shutdown_delay']
  stop_command = f"stop\n"

  for i in range(int(delay) + 1):
    wrapper.server_process.stdin.write(f"say Server will be shutting down in {int(delay) - i} seconds\n")
    wrapper.server_process.stdin.flush()
    time.sleep(1)

  wrapper.server_process.stdin.write(stop_command)
  wrapper.server_process.stdin.flush()
  wrapper.server_process.wait()
  wrapper.log_handler.append("Server has been stopped!")

def help(wrapper):
  wrapper.append_log("Stops the server if it is running after config['shutdown_delay'] seconds")

def summary():
  return "Stops the server."
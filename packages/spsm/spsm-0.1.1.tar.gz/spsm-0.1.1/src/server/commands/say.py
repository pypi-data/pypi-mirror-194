def run(wrapper, *args):
  message = ""
  for m in args:
    message = message + ' ' + m
  wrapper.server_process.stdin(f"/say {str(message)}".encode())
  wrapper.server_process.stdin.flush()

def help(wrapper):
  wrapper.append_log("Broadcasts a message to all the players on the server")

def summary():
  return "Sends message to server."
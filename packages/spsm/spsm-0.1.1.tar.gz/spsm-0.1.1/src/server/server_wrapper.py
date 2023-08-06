from json import load
import os
import re
import time
import errno
import traceback
from threading import Thread

from server.enums.log_levels import LogLevels
from utils.config import load_config
from server.handlers import InputHandler, OutputHandler, LogHandler, ErrorHandler, ScreenHandler


class ServerWrapper:
  def __init__(self):
    self.config = load_config()
    self.screen_name = self.config['screen_name']
    self.server_process = None
    self.threads = {}
    self.active = False

    self.error_handler = ErrorHandler(self.config, self)
    self.input_handler = InputHandler(self.config, self)
    self.output_handler = OutputHandler(self.config, self)
    self.screen_handler = ScreenHandler(self.config, self)
    self.log_handler = LogHandler(self.config, self)
    
    self.initialize_handlers()
  
    self.fifo_input_path = "commander_out_pipe"
    if not os.path.exists(self.fifo_input_path):
      os.mkfifo(self.fifo_input_path)

  def initialize_handlers(self):
    self.error_handler.connect_output(self.output_handler, self.log_handler)
    self.log_handler.connect_output(self.output_handler)
    
    self.input_handler.connect_screen(self.screen_handler)
    self.output_handler.connect_screen(self.screen_handler)
    
    self.log_handler.connect_error_handling(self.error_handler)
    self.input_handler.connect_error_handling(self.error_handler)
    self.output_handler.connect_error_handling(self.error_handler)
    self.screen_handler.connect_error_handling(self.error_handler)
    
    self.screen_handler.connect_input_handler(self.input_handler)
    
    self.screen_handler.connect_log_handling(self.log_handler)
    

  def activate(self):
    try:
      self.active = True
      self.screen_handler.init_windows()
      self.init_threads()

      while self.active:
        pass
      
    except Exception as e:
      self.error_handler.handle_fatal(e)
    finally:
      # self.log_handler.dump_log()
      self.active = False
      # for thread in self.threads.values():
      #   thread.join()
      self.cleanup()

  def deactivate(self):
    self.append_log("Deactivating now...", severity=LogLevels.WARN)
    if self.is_running():
      self.input_handler.handle_command("stop")
      self.server_process.wait()
      
    time.sleep(0.01)
    self.active = False
    time.sleep(0.01)

  def cleanup(self):
    self.screen_handler.cleanup()

  def init_threads(self):
    self.threads['output_processing'] = Thread(target=self.output_handler.process_queue, daemon=True)
    self.threads['input_processing'] = Thread(target=self.input_handler.process_queue, daemon=True)
    self.threads['fifo_reading'] = Thread(target=self.read_fifo_input, daemon=True)
    self.threads['server_output_pipe'] = Thread(target=self.pipe_server_output, daemon=True)
    self.threads['user_input_handling'] = Thread(target=self.screen_handler.track_input, daemon=True)
    
    for name, thread in self.threads.items():
      thread.start()
      time.sleep(0.01)
      self.append_log(f"Initializing thread {name}")
  
  def read_fifo_input(self):
    pipe = os.open(self.fifo_input_path, os.O_RDONLY | os.O_NONBLOCK)
    while self.active:
      try:
        data = os.read(pipe, 50)
        self.input_handler.queue_input(data.decode("utf-8"))
      except OSError as e:
        if e.errno != errno.EAGAIN:
          raise
      except Exception as e:
        self.error_handler.handle_fatal(e)

  def prepare_for_attach(self):
    self.screen_handler.prepare_for_attach()

  def prepare_for_detach(self):
    self.screen_handler.prepare_for_detach()

  def append_log(self, message, source="Main Thread", severity=LogLevels.INFO):
    self.log_handler.append(message, source=source, severity=severity)

  def send_to_server(self, command):
    self.append_log(f"sending: {command} to server")
    self.server_process.stdin.write(command.strip() + '\n')
    self.server_process.stdin.flush()
    
  def pipe_server_output(self):
    server_message_regex = re.compile('\[(\d{2}:\d{2}:\d{2}) (\w+)\]: (?:\[(.+)\] )?(.+$)')
    while self.active:
      if self.is_running():
        for output in self.server_process.stdout:
          groups = server_message_regex.match(output)
          if groups is not None:
            source = groups.group(3)
            severity = groups.group(2)
            message = groups.group(4)
          else:
            source = "Server"
            severity = "Info"
            message = output
            
          if source is None:
            source = 'Server'
          self.append_log(message.strip("\r\n\t "), source=source, severity=LogLevels[severity.upper()])
        for output in self.server_process.stderr:
          self.append_log(output, source="Server", severity=LogLevels.FATAL)

  def reload_config(self):
    self.append_log("Reloading config...")
    self.config = load_config()

  def is_running(self):
    return self.server_process is not None and self.server_process.poll() is None

  def list_commands(self):
    for command, module in self.input_handler.command_modules.items():
      if not hasattr(module, 'summary'):
        continue
      self.append_log(f"{command} -- {module.summary()}")


def main():
  wrapper = ServerWrapper()
  try:
    wrapper.activate()
  except Exception as e:
    wrapper.error_handler.handle_fatal(e)
    print(traceback.format_exc())
    input("Crashing...")
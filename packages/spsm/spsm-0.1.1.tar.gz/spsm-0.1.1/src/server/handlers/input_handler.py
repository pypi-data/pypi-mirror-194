import os
import importlib
import time
from queue import Queue
from threading import Event

from server.enums.log_levels import LogLevels

class InputHandler:
  def __init__(self, config, wrapper):
    self.config = config
    self.wrapper = wrapper
    self.screen_handler = None
    self.error_handler = None
    self.input_queue = Queue()

    self.input_added_event = Event()

    self.command_modules = {}

    command_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'commands'))

    for filename in os.listdir(command_path):
      if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module("server.commands." + module_name, package='commands')
        self.command_modules[module_name] = module

  def connect_screen(self, screen_handler):
    self.screen_handler = screen_handler
    
  def connect_error_handling(self, error_handler):
    self.error_handler = error_handler

  def loop(self):
    while self.wrapper.active:
      window_input = self.screen_handler.get_input()
      if window_input:
        self.queue_input(window_input.strip())

        self.screen_handler.reset_input_window()

  def queue_input(self, input):
    self.input_queue.put(input)
    self.input_added_event.set()

  def process_queue(self):
    try:
      processing_needed = False
      while self.wrapper.active:
        try:
          if processing_needed:
            while not self.input_queue.empty():
              input = self.input_queue.get()
              self.handle_command(input)
          else:
            time.sleep(0.005)

          if self.input_added_event.wait(1):
            self.input_added_event.clear()
            processing_needed = True
        except Exception as e:
          self.error_handler.handle_exception(e)
    except Exception as e:
      self.error_handler.handle_fatal(e)
      
  def handle_command(self, command_input):
    tokens = command_input.split()
    if len(tokens) == 0:
      return
    command = tokens[0]
    args = tokens[1:]

    if command.lower().strip() in self.command_modules.keys():
      self.command_modules[command.lower()].run(self.wrapper, *args)
    elif command.startswith('/'):
      command_string = ""
      for token in tokens:
        command_string = command_string + ' ' + token.strip().replace('/', '')
        
      self.wrapper.send_to_server(command_string)
    else:
      self.wrapper.append_log(f"{command} is not a valid command", "Input Handler", LogLevels.ERROR)
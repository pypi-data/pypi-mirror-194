import traceback

from server.enums.log_levels import LogLevels

class ErrorHandler:
  def __init__(self, config, wrapper):
    self.config = config
    self.log_handler = None
    self.output_handler = None
    self.wrapper = wrapper

  def connect_output(self, output_handler, log_handler):
    self.output_handler = output_handler
    self.log_handler = log_handler

  def handle_fatal(self, exception):
    tb = traceback.format_exc()
    self.log_handler.append(tb, "spsm Error Handler", LogLevels.FATAL)
    self.wrapper.deactivate()
    
  def handle_exception(self, exception):
    tb = traceback.format_exc()
    self.log_handler.append(tb, "spsm Error Handler", LogLevels.ERROR)
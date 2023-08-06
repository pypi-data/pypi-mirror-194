from queue import Queue
from threading import Event
import time

from server.enums.log_levels import LogLevels

class OutputHandler:
  def __init__(self, config, wrapper):
    self.config = config
    self.wrapper = wrapper
    self.screen_handler = None
    self.error_handler = None
    self.output_added_event = Event()
    self.output_queue = Queue()
    
  def connect_screen(self, screen_handler):
    self.screen_handler = screen_handler
    
  def connect_error_handling(self, error_handler):
    self.error_handler = error_handler
    
  def queue_output(self, output, color=0):
    self.output_queue.put([output, color])
    self.output_added_event.set()

  def process_queue(self):
    try:
      output_needed = False
      while self.wrapper.active:
        if output_needed:
          while not self.output_queue.empty():
            output = self.output_queue.get()
            self.screen_handler.append_output(output[0], output[1])
            time.sleep(0.001)
        else:
          time.sleep(0.005)

        if self.output_added_event.wait(1):
          self.output_added_event.clear()
          output_needed = True
    except Exception as e:
      self.error_handler.handle_fatal(e)
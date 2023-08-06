import os
import shutil
import glob
import datetime

from utils import io
from server.enums.log_levels import LogLevels

class LogHandler:
  def __init__(self, config, wrapper):
    self.config = config
    self.wrapper = wrapper
    self.log = []
    self.output_handler = None
    self.error_handler = None
    
    self.archive_latest()
  
  def connect_output(self, output_handler):
    self.output_handler = output_handler
  
  def connect_error_handling(self, error_handler):
    self.error_handler = error_handler
  
  def append(self, message, source="spsm", severity=LogLevels.INFO):
    """
    Add a log entry with the current timestamp, message, and severity level to the log list.

    Args:
        message (str): The log message to add.
        severity (int, optional): The severity level of the log message. 0 is INFO, 1 is WARNING, 
        2 is ERROR, 3 is ALERT, 4 is CRITICAL, and 5 is FATAL. Defaults to 0.
    """
    time = datetime.datetime.now()
    formatted_time = time.strftime("%H:%M:%S")
    log_val = [formatted_time, message, severity, source]
    self.append_file(self.log_to_string(log_val))
    self.log.append(log_val)
    self.output_handler.queue_output(self.log_to_string(log_val), color=severity.value)

  def set_output_handler(self, output_handler):
    self.output_handler = output_handler

  def log_to_string(self, log):
    return f"[{log[0]} {log[2].name}] [{log[3]}]: {log[1]}\n"

  def get_log_as_strings(self):
    log = []
    for line in self.log:
      log.append({'content': self.log_to_string(line), 'color': line[2].value})
      
    return log
  
  def append_file(self, val: str) -> None:
    log_dir = self.config['log_dir']
    
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)

    file_path = os.path.join(log_dir, 'latest.log')
    
    with open(file_path, 'a') as f:
      f.write(val)
      
  
  def dump_log(self):
    log_dir = self.config['log_dir']
    
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)

    file_path = os.path.join(log_dir, 'latest.log')

    self.archive_latest()
      
    with open(file_path, 'w') as f:
      f.write('\n---------- START LOGS\n\n')
      
      for log in self.log:
        f.write(self.log_to_string(log))
      
      f.write('\n\n---------- END LOGS\n')
      
  def archive_latest(self) -> None:
    
    time = datetime.datetime.now()
    formatted_time = time.strftime("[%Y-%m-%d]")
    archive_filename = f'{formatted_time}.zip'
    
    src = os.path.join(self.config['log_dir'], 'latest.log')
    base_dst = os.path.join(self.config['log_dir'], 'archive', archive_filename)

    if not os.path.exists(src):
      return
    
    i = 1
    while True:
      dst = f"{base_dst.split('.')[0]}-{i}.zip"
      if os.path.exists(dst):
        i += 1
      else:      
        io.archive_file(src, dst)
        break
      
import os
import json

from utils.config import load_config
from utils.constants import defaults
from utils import io

class JarDataHandler():
  def __init__(self):
    self.config = load_config()
    self.jars_data = self.load_jar_data()
    
  def touches_jar_data(func):
    def touch_and_save(self, *args, **kwargs):
      val = func(self, *args, **kwargs)
      self.save_jar_data()
      return val
    return touch_and_save
  
  @touches_jar_data
  def upsert_jar_data(self, name, type, url):
    if type != 'server' and type != 'plugin':
      print("Jar must be either of type 'server' or 'plugin'")
      return -1
    
    jar_data = {}
    
    target = f'spsm/jars/plugins/{name}/'
    if type == 'server':
      target = 'spsm/jars/server/'
      
    jar_data['url'] = url
    jar_data['target'] = target
    jar_data['type'] = type
    jar_data['latest_filename'] = None
    
    self.jars_data['data'][name] = jar_data
    
  @touches_jar_data
  def remove_jar_data(self, name):
    del self.jars_data['data'][name]
  
  @touches_jar_data
  def update_jar_filename(self, jar_name, filename):
    self.jars_data['data'][jar_name]['latest_filename'] = filename
  
  def init_jar_data(self, path, filename):
    obj = {}
    obj['version'] = 1
    obj['data'] = {}
    
    io.write_json_file(path, filename, obj)
  
  def jar_names(self):
    return self.jars_data['data'].keys()
  
  def fetch_jar_data(self, name):
    return self.jars_data['data'][name]
  
  def load_jar_data(self):
    path = self.config['jardata_dir']
    filename = self.config['jardata_filename']
    file_path = os.path.join(path, filename)
    if not os.path.exists(file_path):
      self.init_jar_data(path, filename)
    return io.read_json_file(file_path)
    
  def save_jar_data(self):
    path = self.config['jardata_dir']
    filename = self.config['jardata_filename']
    file_path = os.path.join(path, filename)
    if os.path.exists(file_path):
      archive_path = f"{file_path[:-5]}-{self.jars_data['version']}{file_path[-5:]}"
      os.rename(file_path, archive_path)
      self.jars_data['version'] += 1
    io.write_json_file(path, filename, self.jars_data)
    
import os
import shutil

def initialize():
  print("Creating default config file...")
  init_root_files()
  print("Creating spsm directories...")
  init_directories()
  print("Done!")
  
def init_root_files():
  src = os.path.join(os.path.dirname(__file__), 'data', 'spsm.toml')
  shutil.copy(src, 'spsm.toml')
  
def init_directories():
  os.makedirs('spsm', exist_ok=True)
  os.makedirs('spsm/jars', exist_ok=True)
  os.makedirs('spsm/jars/plugins', exist_ok=True)
  os.makedirs('spsm/jars/server', exist_ok=True)
  os.makedirs('spsm/logs', exist_ok=True)
  os.makedirs('spsm/logs/archive', exist_ok=True)
  os.makedirs('spsm/worlds', exist_ok=True)

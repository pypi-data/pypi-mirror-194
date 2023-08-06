import os
import zipfile
import json
from sys import platform

def read_json_file(path):
    if not os.path.exists(path):
        print(f"{path} could not be found.")
        return
    
    obj = {}
    with open(path, 'r') as file:
        obj = json.load(file)
        
    return obj

def write_json_file(path, filename, obj):
    if not os.path.exists(path):
        os.makedirs(path)
        
    file_path = os.path.join(path, filename)
    
    with open(file_path, 'w') as file:
        json.dump(obj, file)

def write_file(target_dir, filename, content):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    file_path = os.path.join(target_dir, filename)
    
    mode = 'w'
    
    if(type(content) == bytes):
        mode = 'wb'
    
    with open(file_path, mode) as f:
        f.write(content)
        
def remove_file(target_dir, filename):
    if not os.path.exists(os.path.join(target_dir, filename)):
        print(f"{target_dir}/{filename} does not exist")
        return
    
    file_path = os.path.join(target_dir, filename)
    
    os.remove(file_path)

def archive_file(src: str, dst: str) -> None:
    """Create an archive of the file at src at dst

    Args:
        src (str): path to the source file directory
        dst (str): path to destination archive file
    """
    if not os.path.exists(src):
        raise FileNotFoundError(src)
    if os.path.isdir(src):
        raise IsADirectoryError(src)
    
    # cwd = os.getcwd()
    # os.chdir(os.path.dirname(src))
    filename = src.split('/')[-1]
    
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as file:
        file.write(src, os.path.basename(src))
        os.remove(src)

    # os.chdir(cwd)

def save_data_file(filename, content):
  # Get the user's home directory
  home_dir = os.path.expanduser("~")
    # Determine the appropriate directory for data files based on the operating system
  if platform == "linux" or platform == "linux2" or platform == "darwin":  # Linux or macOS
      data_dir = os.path.join(home_dir, ".local", "share")
  elif platform == "win32":  # Windows
      data_dir = os.path.join(os.getenv("APPDATA"))
  else:
      print("Unknown operating system")
      return
    
  data_dir = os.path.join(data_dir, 'spsm')
  
  # Create the data directory if it does not exist
  if not os.path.exists(data_dir):
      os.makedirs(data_dir)

  # Create a new file in the data directory
  full_filename = os.path.join(data_dir, filename)
  with open(full_filename, "w") as f:
      f.write(content)
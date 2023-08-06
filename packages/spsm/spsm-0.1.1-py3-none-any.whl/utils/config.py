import tomli

from typing import TypeVar
from collections.abc import Mapping, Iterator

from utils.constants import defaults

T = TypeVar('T')

class Config(Mapping):
  def __init__(self, data: 'dict') -> None:
    super().__init__()
    self._data = data
    
    # Convert any dicts in data into Config objects for safe reading
    for k in self._data.keys():
      if type(self._data[k]) is dict:
        self._data[k] = Config(self._data[k])
  
  def __getitem__(self, __key: str) -> T:
    if __key in self._data.keys():
      return self._data[__key]
    elif hasattr(defaults, __key.upper()):
      return getattr(defaults, __key.upper())
    else:
      return None
  
  def __len__(self) -> int:
    return len(self._data)
  
  def __iter__(self) -> Iterator:
    return iter(self._data)
  
  def __contains__(self, key: str) -> bool:
    return key in self._data.keys()
  
def load_config():
  # if not os.path.exists('./config.ini'):
  #   default_path = os.path.join(os.path.dirname(__file__), 'data', 'default_config.ini')
  #   shutil.copy(default_path, './config.ini')
  with open('./spsm.toml', 'rb') as f:
    config = Config(tomli.load(f))
  # with open('./config.ini', 'r') as f:
  #   for line in f:
  #     key, value = line.strip().split('=')
  #     config[key] = value
  return config
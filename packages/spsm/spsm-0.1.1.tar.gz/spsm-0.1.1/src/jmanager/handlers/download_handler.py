import requests
import re
from utils import config


class DownloadHandler:
  def __init__(self):
    self.config = config.load_config()
    
  def download_from_url(self, url):
    print(f"Downloading from: {url}")
    r = requests.get(url, allow_redirects=True)
    filename = ''
    if "Content-Disposition" in r.headers.keys():
      filename = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
    else:
      filename = url.split("/")[-1]
    return [ filename, r.content ]
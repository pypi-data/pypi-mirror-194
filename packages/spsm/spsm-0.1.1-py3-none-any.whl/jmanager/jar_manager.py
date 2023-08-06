
import os
import glob
import shutil
import click

from utils import config, io
from jmanager.handlers import DownloadHandler, JarDataHandler
from server.server_commander import ServerCommander
from utils.constants import defaults

class JarManager:
  def __init__(self):
    self.config = config.load_config()
    self.jar_data_handler = JarDataHandler()
  
  def ensure_jar_exists(func):
    def jar_exists(self, *args, **kwargs):
      jar_name = args[0]
      if jar_name not in self.jar_data_handler.jar_names():
        print("Jar name not found!")
        return
      return func(self, *args, **kwargs)
    return jar_exists
  
  def upsert_jar(self, name, type='server', url=None):
    return self.jar_data_handler.upsert_jar_data(name, type, url)
  
  @ensure_jar_exists
  def remove_jar(self, jar_name):
    jar_data = self.jar_data_handler.fetch_jar_data(jar_name)
    
    target_dir = jar_data['target']
    filename = jar_data['latest_filename']
    
    print("Removing jar file...", end='')
    io.remove_file(target_dir, filename)
    print("Done.")
    
    print("Removing JarData...", end='')
    self.jar_data_handler.remove_jar_data(jar_name)
    print("Done.")
  
  def update_all_jars(self):
    for jar_name in self.jar_data_handler.jar_names():
      self.update_jar_file(jar_name)
      
    click.secho("All jars updated!", fg='green')
  
  @ensure_jar_exists
  def update_jar_file(self, jar_name, force=False):
    click.secho(f"Updating Jar {jar_name}.", fg='yellow')
    
    jar_data = self.jar_data_handler.fetch_jar_data(jar_name)
    url = jar_data['url']
    
    if url is None:
      click.secho("Jar has no source URL!", fg='red')
      return
    
    dh = DownloadHandler()
    
    filename, file_content = dh.download_from_url(url)
    
    latest_filename = jar_data['latest_filename']
    target_dir = jar_data['target']
    
    
    if not force and latest_filename is not None and latest_filename == filename:
      print(f"Jar {jar_name} is already up to date!")
      return
    elif latest_filename is not None:
      io.remove_file(target_dir, latest_filename)
      
    io.write_file(target_dir, filename, file_content)
    self.jar_data_handler.update_jar_filename(jar_name, filename)
    click.secho(f"Jar {jar_name} has been updated {latest_filename} -> {filename}", fg='yellow')
  
  def jar_present(self, jar_name):
    jar_data = self.jar_data_handler.fetch_jar_data(jar_name)
    target = jar_data['target']
    return len(glob.glob(target + '/*.jar')) > 0
    
  def apply_jar_data(self):
    if ServerCommander(self.config).server_is_active():
      click.secho("Cannot apply jar data while server is active!!", fg='red')
      return
    
    # Ensure jar files have been downloaded and exist
    for jar_name in self.jar_data_handler.jar_names():
      jar_present = self.jar_present(jar_name)
      if not jar_present:
        click.secho(f"No .jar file found for {jar_name}. Attempting to download...", fg='yellow')
        self.update_jar_file(jar_name, force=True)
    
    # Ideally we'd only want to remove files that need to be replaced rather
    # than just removing all of them
    
    # Remove jar files from server directories
    print("Removing jarfiles from server directory...", end='')
    io.remove_file('.', self.config['jar_name'])
    for filename in glob.glob('/plugins/*.jar'):
      os.remove(f'plugins/{filename}')
    print("done")
      
    # Copy jarfiles in storage
    print("Copying jarfiles into server directory...", end='')
    server_filename = glob.glob(f'spsm/jars/server/*.jar')[0]
    plugin_filenames = glob.glob('spsm/jars/plugins/*/*.jar')
    
    shutil.copyfile(server_filename, self.config['jar_name'])
    for filename in plugin_filenames:
      shutil.copyfile(filename, f'plugins/{filename.split("/")[-1]}')
    print('done')
    
    print("Jar configuration has been applied to the server.")
    
  def list_jars(self):
    template = "|{0:18}|{1:18}|{2:80}|"
    header = template.format("JARNAME", "TYPE", "SOURCE URL")
    print('-'*len(header))
    print(header)
    print('-'*len(header))
    for jar_name in self.jar_data_handler.jar_names():
      jar_data = self.jar_data_handler.fetch_jar_data(jar_name)
      url = str(jar_data['url'])
      url = url if len(url) < 80 else url[:77] + "..."
      row = [jar_name, jar_data['type'], url]
      print(template.format(*row))
      print('-'*len(header))
      
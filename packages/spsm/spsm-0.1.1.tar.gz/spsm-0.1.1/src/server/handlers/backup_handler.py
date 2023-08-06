
import os
import shutil
from datetime import datetime
from utils.config import load_config

class BackupHandler:
  def __init__(self):
    self.config = load_config()

  def backup_server(self):
    # Set the server directory and backup directory paths
    server_dir = self.config['server_directory']
    backup_dir = self.config['backup_directory']

    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Archive the server world directory
    backup_file = os.path.join(backup_dir, f"world_{timestamp}.zip")
    shutil.make_archive(backup_file[:-4], "zip", server_dir)

    # Clean up old backup files (keep only the 24 most recent backups)
    backup_files = os.listdir(backup_dir)
    backup_files.sort()
    while len(backup_files) > 24:
        old_backup_file = os.path.join(backup_dir, backup_files.pop(0))
        os.remove(old_backup_file)

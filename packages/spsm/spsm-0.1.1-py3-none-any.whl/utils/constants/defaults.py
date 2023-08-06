from logging import shutdown


# Basic server config
JAR_NAME = 'server.jar'
START_COMMAND = 'java -Xms2G -Xmx2G -jar (jar_name) nogui'
SCREEN_NAME = 'minecraft_server'
SHUTDOWN_DELAY = 60

# Jarfile config
JARDATA_DIR = 'spsm/jardata'
JARDATA_FILENAME = 'jardata.json'

# Log config
LOG_DIR = 'spsm/logs'
MAX_LOG_ARCHIVES = 10

# Backup Config
BACKUP_DIR = 'spsm/backups'
MAX_BACKUPS = 5
import click
import cli
from server.server_commander import ServerCommander
from jmanager import JarManager
from utils.config import load_config

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(cli.__version__, "--version", "-v", message="Simple Python Server Manager, v%(version)s")
def spsm():
    pass

# ----- General Functions ----- #

@spsm.command()
def init():
    """Inititialize the current directory as an spsm managed server
    """
    cli.initialize()
    
@spsm.command(no_args_is_help=True)
@click.argument('resource', type=click.Choice(['jars', 'worlds'], case_sensitive=False))
def list(resource):
    """Lists RESOURCE
    """
    if resource.lower() == 'jars':
        jar_manager = JarManager()
        jar_manager.list_jars()
    elif resource.lower() == 'worlds':
        pass

# ----- Server Functions ----- #

@spsm.group()
def server():
    """Server related commands
    """
    pass

@server.command()
@click.option('-a', '--attach', is_flag=True, help='Immediately attach to the activated server')
@click.option('-d', '--debug', is_flag=True, help='Toggles debug mode')
def activate(attach, debug):
    """Activates the Minecraft server wrapper."""
    config = load_config()
    commander = ServerCommander(config)
    commander.activate_server(debug)
    if attach:
        commander.attach_server()

@server.command()
def start():
    """Starts the Minecraft Server
    """
    config = load_config()
    commander = ServerCommander(config)
    commander.start_server()

@server.command()
def console():
    """Opens an interactive console to interact with the server
    """
    config = load_config()
    commander = ServerCommander(config)
    commander.attach_server()

@server.command()
def stop():
    """Stops the Minecraft Server
    """
    config = load_config()
    commander = ServerCommander(config)
    commander.stop_server()


@server.command()
def restart():
    """Restarts the Minecraft Server
    """
    config = load_config()
    commander = ServerCommander(config)
    commander.restart_server()


@server.command()
@click.argument('command')
def send(command):
    """Sends COMMAND to the Minecraft server Wrapper
    """
    config = load_config()
    commander = ServerCommander(config)
    commander.send_command(command)


@server.command()
def logs():
    """Tail the latest log file.
    """
    config = load_config()
    commander = ServerCommander(config)
    commander.tail_logs()
    
@server.command()
def status():
    """Get the status of the server
    """
    config = load_config()
    commander = ServerCommander(config)
    commander.print_status()

# ----- Jarfile Functions ----- #

@spsm.group()
def jars():
    """Jarfile related commands
    """
    pass
  
@jars.command()
@click.argument('type', type=click.Choice(['server', 'plugin']))
@click.argument('jar-name', type=str)
@click.option('-u', '--source-url', required=False, type=str, default=None, help='URL from which the jar will be downloaded')
@click.option('-a', '--apply', is_flag=True, default=False, help='immediately apply the jardata after the upsert')
def upsert(type, jar_name, source_url, apply):
    """
    Adds jar called JAR_NAME as a TYPE or
    updates it if it already exists
    """
    jar_manager = JarManager()
    if jar_manager.upsert_jar(jar_name, type, source_url) == -1:
        click.secho("Could not upsert jar!", fg='red')
        return
    
    print(f"Jar: {jar_name} has been added.")
    if apply:
        jar_manager.apply_jar_data()
    else:
        click.secho("Jar data must be applied before server is updated!", fg='yellow')

@jars.command()
def apply():
    """apply the current state of jardata to the server
    """
    jar_manager = JarManager()
    jar_manager.apply_jar_data()
    
@jars.command()
@click.option('-a', '--all', default=True, help='download all jars')
@click.option('-j', '--jar-name', type=str, help='name of a specific jar to download')
def download(all, jar_name):
    """
    Downloads the jarfile for either all jars or the given jar based on its source URL
    """
    jar_manager = JarManager()
    if jar_name is not None:
        jar_manager.update_jar_file(jar_name)
    elif all:
        jar_manager.update_all_jars()
    else:
        click.secho("Nothing downloaded.")

# ----- World Management Functions ----- #

@spsm.group()
def worlds():
    """World related commands
    """
    pass

if __name__ == '__main__':
    spsm()

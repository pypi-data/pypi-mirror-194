import click
import subprocess
import os


class ServerCommander:
    """
    Class to handle commands for a server.

    Args:
      config (dict): A dictionary of configuration options for the server.
    """

    def __init__(self, config):
        """
        Initialize the ServerCommander.

        Args:
          config (dict): A dictionary of configuration options for the server.
        """
        self.config = config
        self.screen_name = self.config['screen_name']
        self.fifo_output_path = "commander_out_pipe"

        # Create a named pipe (FIFO) for output
        if not os.path.exists(self.fifo_output_path):
            os.mkfifo(self.fifo_output_path)

    def activate_server(self, debug=False):
        """
        Activate the server using a detached screen with the ServerWrapper activated.
        """
        
        screen_name = self.config['screen_name']

        if self.server_is_active():
            print(f"A screen with name '{screen_name}' is already running.")
            return

        # Start a detached screen with the ServerWrapper activated
        server_wrapper_cmd = f"spsm_server" if not debug else "../venv/bin/spsm_server"
        screen_cmd = f"screen -dmS {screen_name} {server_wrapper_cmd}"
        if debug:
            print("Activating in debug mode!")
            f = open('spsm-debug.txt', 'w')
            subprocess.call(screen_cmd, shell=True, stdout=f, stderr=f)
        else:
            subprocess.call(screen_cmd, shell=True)

        if self.server_is_active():
            print("Server Activated!")
        else:
            print("Failed to activate server.")

    def print_status(self):
        if self.server_is_active():
            click.secho("Server is Active", fg='green')
        else:
            click.secho("Server is not Active", fg='yellow')
    
    def server_is_active(self):
        """
        Check if the server is currently active.

        Returns:
            bool: True if the server is active, False otherwise.
        """
        screen_name = self.config['screen_name']
        try:
            check_screen_cmd = f"screen -list | grep -w {screen_name}"
            subprocess.check_output(
                check_screen_cmd, shell=True, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False

    def attach_server(self):
        """
        Attach to the server's screen session.
        """
        if not self.server_is_active():
            print('Server has not been activated.')
            return
        screen_name = self.config['screen_name']
        try:
            process = subprocess.Popen(['screen', '-r', screen_name])
            with open(self.fifo_output_path, 'w') as pipe:
                pipe.write('prepare_for_attach')
            process.wait()
        except subprocess.CalledProcessError:
            print(f"No screen found with name {screen_name}")

    def start_server(self):
        """
        Send a command to the server to start it.
        """
        with open(self.fifo_output_path, 'w') as pipe:
            pipe.write('start')

    def stop_server(self):
        """
        Send a command to the server to stop it.
        """
        with open(self.fifo_output_path, 'w') as pipe:
            pipe.write('stop')

    def restart_server(self):
        """
        Send a command to the server to restart it.
        """
        with open(self.fifo_output_path, 'w') as pipe:
            pipe.write('restart')

    def send_command(self, command, *args):
        """
        Send a command to the server.

        Args:
            command (str): The command to send to the server.
            *args: Any additional arguments to include with the command.
        """
        command_string = command
        for arg in args:
            command_string = command_string + ' ' + str(arg)
        with open(self.fifo_output_path, 'w') as pipe:
            pipe.write(command_string)

    def tail_logs(self):
        """
        Tail the server's log file in the terminal.
        """
        log_file = os.path.join(
            self.config['log_dir'], "latest.log")
        tail_command = f'tail -n 100 {log_file}'
        subprocess.run(tail_command, shell=True)
        print()

from .password_helper import get_root_password
from dataclasses import dataclass
from . import config 

import subprocess

@dataclass
class CommandHandler:
    logger = config.get_logger(__name__)
    logger.info("create instance of CommandHandler")

    def run_shell_command_with_input(self, command: str, input: str=''):
        """run shell command as root .eg. with password as input

        Args:
            command (str): the shell command to run
            input (str): input
        """
        self.logger.debug("run_shell_command_with_input() func is called")
        process = subprocess.run(
            [f"su -c '{command}'"],
            shell=True,
            input=f"{input}\n",
            capture_output=True,
            encoding="utf-8",
            timeout=6,
        )
        self.logger.debug(
            f"process is created: stdout: {process.stdout} || stderr: {process.stderr}"
        )
        return process

    def run_shell_command(self, command: str):
        """ run shell command simple usage"""
        self.logger.debug("run_shell_command() func is called")
        process = subprocess.run(
            [f"{command}"],
            shell=True,
            capture_output=True,
            encoding="utf-8",
            timeout=6,
        )
        self.logger.debug(
            f"process is created: stdout: {process.stdout} || stderr: {process.stderr}"
        )
        return process


    def run_shell_command_as_root(self, command: str):
        """Run a shell command as the root user in Linux.

        Args:
            command (str): The shell command to run.

        Returns:
            None
        """
        self.logger.debug("run_shell_command_as_root() function called")
        if get_root_password() == None:
            raise RuntimeError("ROOT_PASSWORD is not is PATH.")

        try:
            self.run_shell_command_with_input(command, get_root_password())
        except Exception as e: 
            raise RuntimeError(f"Error running shell command: {e}")
        else:
            self.logger.debug(f"Shell command run as root successfully. command: {command}")


if __name__ == "__main__":
    ch = CommandHandler()
    ch.run_shell_command_as_root("notify-send 'hello'")
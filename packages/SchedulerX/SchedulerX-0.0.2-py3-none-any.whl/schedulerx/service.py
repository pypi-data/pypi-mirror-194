from .file_manager import FileManager
from . import config


class ServiceManager:
    """Service class manages: create the service file
    Args:
        filename (string): name of the service file with extension
        command (string): command to run
    """

    def __init__(
        self,
        filename: str,
        command: str,
        description: str = "",
        overwrite: bool = False,
    ):
        self.filename: str = filename
        # todo: set a default description: title or the first part of filename
        # todo: "title" service
        self.description = description
        self.command = command
        self.overwrite = overwrite

        self.logger = config.get_logger(__name__)
        self.logger.info("create an instance of ServiceManager")

    def create_service_file(self):
        self.logger.info("create service file")
        self.file_manager = FileManager(self.filename, overwrite=self.overwrite)
        self.file_manager.create_file(content=self._get_service_text())
        self.logger.info("created service file")

    def _get_service_text(self):
        return f"""[Unit]
Description={self.description}


[Service]
User=root
ExecStart={self.command}
"""


if __name__ == "__main__":
    service_manager = ServiceManager(
        filename="test.service", command="screensaver-command -l"
    )
    service_manager.create_service_file()

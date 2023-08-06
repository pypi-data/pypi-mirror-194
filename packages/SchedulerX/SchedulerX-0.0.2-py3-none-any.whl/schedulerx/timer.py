from .file_manager import FileManager
from .service import ServiceManager
from .run_command import CommandHandler
from . import config

import os


class TimerManager:
    """

    Args:
        service_manager (ServiceManager): service manager instance linked to
        to this timer instance
        description (str): timer_description
    """

    def __init__(
        self,
        filename: str,
        on_calendar: str,
        service_manager: ServiceManager,
        description: str = "",
        overwrite: bool = False,
    ) -> None:
        self.logger = config.get_logger(__name__)
        self.logger.info("created instance of TimerManager")

        self.filename = filename
        self.description = description
        self.on_calendar = on_calendar
        self.service_manager: ServiceManager = service_manager
        self.overwrite = overwrite

        self.file_manager = FileManager(filename=self.filename, overwrite=self.overwrite)
        self.command_handler = CommandHandler()

    def create_timer(self):
        self.logger.debug(f"create timer file {self.filename}")
        self.file_manager.create_file(self._get_timer_text())
        self.logger.info(f"created timer file {self.filename}")

    def _get_timer_text(self):
        return f"""[Unit]
Description={self.description}
Requires={self.service_manager.filename}


[Timer]
OnCalendar={self.on_calendar}
Unit={self.service_manager.filename}

[Install]
WantedBy=multi-user.target
"""

    def start_timer(self):
        # reload daemon process
        self.logger.debug("reload daemon process")
        self.command_handler.run_shell_command_as_root("systemctl daemon-reload")
        # start timer
        self.logger.debug("start timer")
        self.command_handler.run_shell_command_as_root(
            f"systemctl start {self.filename}"
        )

        self.logger.debug("enable timer")
        self.command_handler.run_shell_command_as_root(
            f"systemctl enable {self.filename}"
        )

        self.logger.info("timer is set successfully")


if __name__ == "__main__":
    title = "tes"
    sm = ServiceManager(f"{title}.service", "ls")
    sm.create_service_file()
    tm = TimerManager(f"{title}.timer", on_calendar="12:12:12", service_manager=sm)
    tm.create_timer()
    os.remove(f"/etc/systemd/system/{title}.service")
    os.remove(f"/etc/systemd/system/{title}.timer")

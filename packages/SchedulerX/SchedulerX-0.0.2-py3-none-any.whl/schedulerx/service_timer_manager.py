from .timer import TimerManager
from .service import ServiceManager

from dataclasses import dataclass


@dataclass(kw_only=True)
class ServiceTimerManager:
    # todo: manage directory when you put services and timers.
    service_filename: str 
    service_description: str = ""
    command: str

    timer_filename: str
    timer_description: str = ""
    on_calendar: str
    
    overwrite: bool = False

    def schedule(self):
        self._create_service()
        self._create_timer()
        self.timer_manager.start_timer()

    def _create_service(self):
        self.service_manager = ServiceManager(
            filename=self.service_filename, 
            description=self.service_description, 
            command=self.command,
            overwrite=self.overwrite,
        )
        self.service_manager.create_service_file()

    def _create_timer(self):
        self.timer_manager = TimerManager(
            filename=self.timer_filename,
            description=self.timer_description,
            on_calendar=self.on_calendar,
            service_manager=self.service_manager,
            overwrite=self.overwrite,
        )
        self.timer_manager.create_timer()
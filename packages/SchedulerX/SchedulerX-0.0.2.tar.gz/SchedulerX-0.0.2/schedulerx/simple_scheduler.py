from .service_timer_manager import ServiceTimerManager
from . import config

class SimpleScheduler:
    def __init__(self, title: str, command: str, on_calendar: str, overwrite: bool = False):
        self.logger = config.get_logger(__class__.__name__)
        self.logger.info("create instance of SimpleScheduler")

        self.title = title
        self.command = command
        self.on_calendar = on_calendar
        self.overwrite = overwrite
    
    def schedule(self):
        self.logger.info("create instance of ServiceTimerManager")
        self.service_timer_manager = ServiceTimerManager(
            service_filename=f"{self.title.replace(' ', '_')}.service",
            service_description=self.title,
            command=self.command,
            timer_filename=f"{self.title.replace(' ', '_')}.timer",
            timer_description=self.title,
            on_calendar=self.on_calendar,
            overwrite=self.overwrite,
        )
        self.logger.info("created instance of ServiceTimerManager")
        self.service_timer_manager.schedule()
        self.logger.info("schedule complete")

        
if __name__ == '__main__':
    import os 
    title='testing simple scheduler'
    title = title.replace(' ', '_')
    sc = SimpleScheduler(
        title=title,
        command='shutdown now',
        on_calendar='daily',
        overwrite=True,
    )
    sc.schedule()
    os.remove(f'/etc/systemd/system/{title}.service')
    os.remove(f'/etc/systemd/system/{title}.timer')   
from schedulerx import ServiceTimerManager

service_timer = ServiceTimerManager(
    service_filename="shutdown.service",
    service_description="shutdown at midnight",
    command="shutdown now",
    timer_filename="shutdown.timer",
    timer_description="shutdown at midnight timer",
    on_calendar="@daily",
)
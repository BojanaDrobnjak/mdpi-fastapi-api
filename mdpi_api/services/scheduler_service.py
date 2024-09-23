from typing import Any, Callable, Union

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, JobExecutionEvent
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.base import BaseTrigger
from loguru import logger
from mdpi_api.settings import settings


class SchedulerManager:
    """Scheduler manager."""

    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler(
            jobstores={"default": MemoryJobStore()},
            timezone="UTC",
        )
        self.scheduler.add_listener(
            self.job_listener,
            EVENT_JOB_MISSED | EVENT_JOB_ERROR,
        )

    def add_job(
        self,
        func: Callable[..., Any],
        trigger: Union[str, BaseTrigger],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Add job to the scheduler.

        :param func: The function to run.
        :param trigger: The trigger type.
        :param args: The function arguments.
        :param kwargs: The function keyword arguments.
        """
        self.scheduler.add_job(func, trigger, *args, **kwargs)

    def start(self) -> None:
        """Start the scheduler."""
        self.scheduler.start()

    def shutdown(self) -> None:
        """Shutdown the scheduler."""
        self.scheduler.shutdown()

    @staticmethod
    def job_listener(event: JobExecutionEvent) -> None:
        """
        Listener for job events.

        :param event: Job event.
        """
        job_id = event.job_id
        scheduled_run_time = event.scheduled_run_time

        if event.code == EVENT_JOB_ERROR:
            message = (
                f"Job {job_id} encountered an error at {scheduled_run_time}.\n"
                f"Exception: {event.exception}"
            )
            logger.error(message)
        elif event.code == EVENT_JOB_MISSED:
            message = (
                f"Job {job_id} was scheduled to run at {scheduled_run_time} but missed."
            )
            logger.warning(message)
        else:
            return

        if settings.environment == "prod":
            # TODO: Implement alerting
            return

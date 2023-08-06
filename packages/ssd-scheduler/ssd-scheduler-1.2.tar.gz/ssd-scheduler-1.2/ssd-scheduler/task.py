import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Hashable, Optional, Tuple

from croniter import croniter


class Task:

    def __init__(
        self,
        name: str,
        cron_schedule: str,
        job: Callable,
        job_args: Optional[Tuple[Any, ...]] = None,
        job_kwargs: Optional[Dict[Hashable, Any]] = None,
        *,
        is_overdue_gap_needed: bool = True,
    ):
        self._name = name
        self._instance_key = uuid.uuid4()
        self._job = job

        # Не рекомендуется использовать мутирующие объекты в качестве аргументов
        self._job_args = job_args or ()
        self._job_kwargs = job_kwargs or {}
        self._cron_schedule = cron_schedule

        self._croniter = self._create_calendar()
        self._is_overdue_gap_needed = is_overdue_gap_needed

        self._next_run = self._croniter.get_next(datetime)
        self._last_started_at = None

        self._logger = logging.getLogger(f'{"TODO"}.task')  #TODO

    def __str__(self) -> str:
        return (
            f'Task with job [{repr(self._job)}] '
            f'and cron schedule [{self._cron_schedule}]'
        )

    def get_name(self) -> str:
        return self._name

    def get_uniq_name(self) -> str:
        return f'{self._name}_{self._instance_key}'

    def get_job(self) -> Callable:
        return self._run

    def get_next_run_datepoint(self) -> datetime:
        return self._next_run

    def _run(self):
        self._logger.info(
            'Task [%s] started with schedule [%s]',
            self._name,
            self._cron_schedule,
        )

        self._last_started_at = datetime.now(timezone.utc)
        try:
            self._job(*self._job_args, **self._job_kwargs)
        except Exception:
            self._logger.exception(
                'Unexpected error occurred in task [%s]',
                self._name,
            )
        else:
            self._logger.info(
                'Task completed [%s]',
                self._name,
            )

        self._on_finish()

    def _on_finish(self):
        finished_at = datetime.now(timezone.utc)

        optimistic_next_run = self._croniter.get_next(
            datetime,
            self._croniter.get_current(),
        )

        is_overdue = finished_at >= optimistic_next_run
        if not is_overdue:
            self._next_run = optimistic_next_run

        if is_overdue and self._is_overdue_gap_needed:
            self._croniter.set_current(finished_at)
            self._next_run = self._croniter.get_next(datetime)

        if is_overdue and not self._is_overdue_gap_needed:
            self._croniter.set_current(finished_at)
            self._next_run = finished_at

    def _create_calendar(self) -> croniter:
        assert croniter.is_valid(self._cron_schedule), 'No valid cron schedule'
        return croniter(self._cron_schedule, datetime.now(timezone.utc))

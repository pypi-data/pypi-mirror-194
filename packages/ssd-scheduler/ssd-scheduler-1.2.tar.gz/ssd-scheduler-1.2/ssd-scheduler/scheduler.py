import heapq
import logging
import signal
import time
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timezone
from threading import Lock
from typing import List, Tuple

from .task import Task


class Scheduler:
    _loop_delay: float = 0.01

    def __init__(self, *tasks: Task):
        self._stopped = False
        self._tasks = tasks
        self._lock = Lock()

        assert len(tasks) > 0
        assert len(tasks) == len(
            set(task.get_name() for task in tasks)
        ), 'Task names should be unique'

        self._executor = ThreadPoolExecutor(
            max_workers=len(tasks),
            thread_name_prefix='scheduler',
        )
        self._tasks_q: List[Tuple[datetime, str, Task]] = []
        self._prepare_tasks(*tasks)
        self._futures_mapper = {}

        self._logger = logging.getLogger('scheduler_mapper')

        self._register_sigterm_handler()

    def _register_sigterm_handler(self):

        def new_handler(*args, **kwargs):
            self.stop()

            if isinstance(old_handler, Callable):
                old_handler(*args, **kwargs)

        old_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, new_handler)

    def stop(self):
        self._logger.info('Trying to gracefully stop scheduler')
        self._stopped = True
        self._logger.info('Waiting for all pending tasks...')
        self._executor.shutdown(wait=True)
        self._logger.info('Stopping done')

    @property
    def is_stopped(self):
        return self._stopped

    def run(self):
        while not self._stopped:
            try:
                self._run()
            except (KeyboardInterrupt, SystemExit):
                self.stop()
                continue
            except Exception:
                self._logger.exception(
                    'Unexpected error occurred, trying again'
                )
                time.sleep(self._loop_delay)
                continue

    def _run(self):
        while not self._stopped:
            if len(self._tasks_q) == 0:
                time.sleep(self._loop_delay)
                continue

            with self._lock:
                next_task = self._peak_nearest_task()
                next_run = next_task.get_next_run_datepoint()

                utcnow = datetime.now(timezone.utc)
                next_run_delay = (next_run - utcnow).total_seconds()

                if next_run_delay > 0:
                    time.sleep(self._loop_delay)
                    continue

                self._pop_nearest_task()
            self._run_task(next_task)

    def _peak_nearest_task(self) -> Task:
        return self._tasks_q[0][2]

    def _pop_nearest_task(self):
        heapq.heappop(self._tasks_q)

    def _push_task(self, task: Task):
        with self._lock:
            heapq.heappush(
                self._tasks_q, (
                    task.get_next_run_datepoint(),
                    task.get_uniq_name(),
                    task,
                )
            )

    def _prepare_tasks(self, *tasks: Task):
        for task in tasks:
            self._update_task_schedule(task)

    def _on_task_done(self, future: Future):
        task = self._futures_mapper[id(future)]
        self._update_task_schedule(task)

    def _update_task_schedule(self, task: Task):
        self._push_task(task)

    def _run_task(self, task: Task) -> None:
        # Это случается, если прилетает sigterm
        if self._stopped:
            self._logger.info('Scheduler is stopped, cancel task')
            return

        job = task.get_job()

        future = self._executor.submit(job)
        self._futures_mapper[id(future)] = task
        future.add_done_callback(self._on_task_done)

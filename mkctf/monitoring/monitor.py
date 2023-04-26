"""mkctf monitor implementation
"""
import typing as t
from asyncio import (
    Task,
    Queue,
    CancelledError,
    sleep,
    gather,
    create_task,
)
from dataclasses import dataclass, field
from humanize import naturaldelta
from .task import MonitorTask
from .notifier import MonitorNotifier
from ..api import MKCTFAPI
from ..helper.logging import LOGGER


@dataclass
class MKCTFMonitor:
    """[summary]"""

    mkctf_api: MKCTFAPI
    notifier: MonitorNotifier
    count: int = -1
    delay: int = 600
    timeout: int = 120
    worker: int = 4
    _queue: Queue = field(default_factory=Queue)
    _tasks: t.List[Task] = field(default_factory=list)

    async def _task_routine(self, worker_id):
        """Represent a monitoring task"""
        while True:
            task = await self._queue.get()
            if task is None:
                LOGGER.info("[%s]: exiting gracefully", worker_id)
                break
            countdown = task.countdown(self.delay)
            if countdown > 0:
                LOGGER.info(
                    "[%s]: waiting for %s before running %s",
                    worker_id,
                    task.slug,
                    naturaldelta(countdown),
                )
                await sleep(countdown)
            LOGGER.info(
                "[%s]: running healthcheck for %s", worker_id, task.slug
            )
            cpr = None
            try:
                cpr = await task.run()
            except:
                LOGGER.exception(
                    "[%s]: an exception occured while running healthcheck for %s",
                    worker_id,
                    task.slug,
                )
            LOGGER.info(
                "[%s]: healthcheck took %s for %s",
                worker_id,
                naturaldelta(task.duration),
                task.slug,
            )
            if cpr is None:
                await self.notifier.post(worker_id, task.slug, False)
            else:
                await self.notifier.post(worker_id, task.slug, cpr.healthy)
            if self.count > 0 and task.count < self.count:
                await self._queue.put(task)
            self._queue.task_done()

    async def run(self):
        """[summary]"""
        for challenge_api in self.mkctf_api.enum():
            slug = challenge_api.config.slug
            if not challenge_api.config.enabled:
                LOGGER.info("[monitor]: %s skipped (disabled)", slug)
                continue
            LOGGER.info("[monitor]: injecting a task for %s", slug)
            await self._queue.put(
                MonitorTask(
                    mkctf_api=self.mkctf_api, slug=slug, timeout=self.timeout
                )
            )
        # check if queue is empty before starting
        if self._queue.empty():
            LOGGER.info("[monitor]: no task to process, exiting.")
            return
        # create N worker tasks to process the queue concurrently
        LOGGER.info("[monitor]: spawning %d workers...", self.worker)
        for k in range(self.worker):
            task = create_task(self._task_routine(f'task-{k}'))
            self._tasks.append(task)
        # await queue to be processed entirely
        LOGGER.info("[monitor]: waiting for tasks to be processed...")
        try:
            await self._queue.join()
        except CancelledError:
            LOGGER.warning("[monitor]: tasks cancelled.")
        # terminate workers
        LOGGER.info("[monitor]: terminating workers...")
        for _ in self._tasks:
            await self._queue.put(None)
        # await workers termination
        LOGGER.info("[monitor]: waiting for workers to terminate...")
        await gather(*self._tasks, return_exceptions=True)
        LOGGER.info("[monitor]: exiting.")

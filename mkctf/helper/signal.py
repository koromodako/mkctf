"""Signal module
"""

from asyncio import all_tasks, create_task, current_task, gather
from signal import SIGHUP, SIGINT, SIGTERM

from .logging import LOGGER

HANDLED_SIGNALS = (SIGHUP, SIGTERM, SIGINT)


async def _shutdown(_, loop):
    print()
    LOGGER.info("termination query received")
    tasks = [task for task in all_tasks() if task is not current_task()]
    _ = [task.cancel() for task in tasks]
    LOGGER.warning("waiting for tasks to terminate... please wait")
    await gather(*tasks)
    loop.stop()
    LOGGER.info("finally exiting")


def setup_signals_handler(loop):
    """Setup termination signals handlers"""
    for signal in HANDLED_SIGNALS:
        loop.add_signal_handler(
            signal, lambda signal=signal: create_task(_shutdown(signal, loop))
        )

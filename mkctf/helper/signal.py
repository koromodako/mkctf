# ==============================================================================
#  IMPORTS
# ==============================================================================
from signal import SIGHUP, SIGTERM, SIGINT
from asyncio import all_tasks, current_task, gather, create_task
from .log import app_log
# ==============================================================================
#  GLOBALS
# ==============================================================================
HANDLED_SIGNALS = (SIGHUP, SIGTERM, SIGINT)
# ==============================================================================
#  FUNCTIONS
# ==============================================================================
async def _shutdown(signal, loop):
    app_log.info("termination query received")
    tasks = [task for task in all_tasks() if task is not current_task()]
    [task.cancel() for task in tasks]
    app_log.warning("waiting for tasks to terminate... please wait")
    await gather(*tasks)
    loop.stop()
    app_log.info("finally exiting")

def setup_signals_handler(loop):
    '''[summary]
    '''
    for signal in HANDLED_SIGNALS:
        loop.add_signal_handler(signal, lambda signal=signal: create_task(_shutdown(signal, loop)))

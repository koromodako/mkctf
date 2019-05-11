# =============================================================================
#  IMPORTS
# =============================================================================
from time import time
from asyncio import sleep
from mkctf.api import MKCTFAPI
# =============================================================================
#  CLASSES
# =============================================================================
class MonitorTask:
    '''Monitoring task

    It provides methods for:
     - retrieving the slug of the associated challenge: self.slug
     - retrieving latest execution duration: self.duration
     - dertermine if the task should run again: self.should_run_again
     - sleeping some time before next execution: self.sleep()
     - running the task: self.run()
    '''
    def __init__(self, monitor, slug):
        '''Construct a task
        '''
        self._slug = slug
        self._monitor = monitor
        self._start = 0
        self._duration = 0
        self._iter_cnt = 0

    @property
    def slug(self):
        '''Retrieve the slug of the challenge
        '''
        return self._slug

    @property
    def duration(self):
        '''Retrieve the duration of the latest run (in seconds)
        '''
        return self._duration

    @property
    def countdown(self):
        remaining = self._monitor.iter_delay - (int(time()) - self._start)
        return max(0, remaining)

    @property
    def should_run_again(self):
        '''Determine if the task should run again
        '''
        if self._monitor.iter_cnt > 0:
            return self._iter_cnt < self._monitor.iter_cnt
        return True

    async def is_ready(self):
        '''Sleep for some time
        '''
        remaining = self.countdown
        if remaining > 0:
            await sleep(remaining)

    async def run(self):
        '''Run the task
        '''
        # reset start time
        self._start = int(time())
        # increment count if needed
        self._iter_cnt += 1
        # run exploit using mkCTF API
        async for report in self._monitor.healthcheck(self.slug):
            healthy = report['rcode'] in MKCTFAPI.HEALTHY_RCODES
            report['healthy'] = healthy
            self._duration = int(time()) - self._start
            return report
        return None

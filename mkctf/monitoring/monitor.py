# =============================================================================
#  IMPORTS
# =============================================================================
import sys
from time import time
from asyncio import (
    get_event_loop,
    create_task,
    gather,
    Queue,
    Lock,
)
from aiohttp import ClientSession, ClientTimeout, BasicAuth
from humanize import naturaldelta
from mkctf.helper.log import app_log
from .task import MonitorTask
# =============================================================================
#  FUNCTIONS
# =============================================================================
def raw_print(output, data):
    '''Prints raw 'data' to 'output'
    '''
    output.buffer.write(data if data else b'[empty]\n')
    output.buffer.flush()

async def worker_routine(worker_id, monitor):
    '''Represent a monitoring worker
    '''
    while True:
        # get next exploit_task out of the queue
        task = await monitor.task_queue.get()
        if task is None:
            await monitor.print(f"[{worker_id}]: exiting gracefully")
            break
        # process exploit_task
        await monitor.print(f"[{worker_id}]: waiting for {task.slug} to reach schedule")
        await task.is_ready()
        await monitor.print(f"[{worker_id}]: running exploit for {task.slug}")
        try:
            report = await task.run()
        except:
            report = None
            await monitor.post(task.slug, False)
            await monitor.print(f"[{worker_id}]: an exception occured while running {task.slug}")
        # inject exploit back in queue if needed
        if task.should_run_again:
            await monitor.task_queue.put(task)
        # notify the queue that the exploit_task has been processed
        monitor.task_queue.task_done()
        # print report
        if report:
            stdout = b''
            stderr = b''
            health = 'healthy' if report['healthy'] else 'DEAD'
            text = '=' * 80
            text += '\n'
            text += f"[{worker_id}]: reporting for {task.slug}\n"
            text += f"[{worker_id}]:  - state: {health}\n"
            text += f"[{worker_id}]:  - check duration: {naturaldelta(task.duration)}\n"
            if not report['healthy']:
                stdout = f"----------------[{task.slug}:STDOUT]----------------\n"
                stdout = stdout.encode() + report['stdout']
                stderr = f"----------------[{task.slug}:STDERR]----------------\n"
                stderr = stderr.encode() + report['stderr']
            text = text.encode() + stdout + stderr
            await monitor.print(text, raw=True)
# =============================================================================
#  CLASSES
# =============================================================================
class MKCTFMonitor:
    '''[summary]
    '''
    def __init__(self, api, host, port, username, password,
                 iter_cnt=-1, iter_delay=600,
                 task_timeout=120, worker_cnt=4,
                 post_timeout=60, no_verify_ssl=False):
        '''[summary]
        '''
        self._api = api
        self._workers = []
        self._iter_cnt = iter_cnt
        self._iter_delay = iter_delay
        self._worker_cnt = worker_cnt
        self._task_queue = Queue()
        self._task_timeout = task_timeout
        self._output_lock = Lock()
        self._url = f'https://{host}:{port}/mkctf-api/healthcheck'
        self._ssl = False if no_verify_ssl else None
        self._auth = BasicAuth(username, password)
        self._post_timeout = ClientTimeout(timeout=post_timeout)

    @property
    def task_queue(self):
        return self._task_queue

    @property
    def iter_cnt(self):
        return self._iter_cnt

    @property
    def iter_delay(self):
        return self._iter_delay

    async def run(self):
        '''[summary]
        '''
        for challenge in self._api.enum():
            if not challenge['conf']['enabled']:
                app_log.warning(f"{challenge['slug']} skipped (disabled)")
                continue
            app_log.info(f"injecting a task for {challenge['slug']}...")
            await self._task_queue.put(MonitorTask(self, challenge['slug']))
        # create 4 worker tasks to process the queue concurrently
        for k in range(self._worker_cnt):
            worker = create_task(worker_routine(f'worker-{k}', self))
            self._workers.append(worker)
        # await queue to be processed entirely
        await self._task_queue.join()
        # terminate workers
        for _ in self._workers:
            await self._task_queue.put(None)
        # await workers termination
        await gather(*self._workers, return_exceptions=True)

    async def print(self, data, raw=False):
        '''Print a message without interruption by a concurrent

        if 'output_buf' is set to sys.stdout or sys.stderr then 'data' must be bytes
        else data must be str
        '''
        async with self._output_lock:
            if raw:
                sys.stdout.buffer.write(data if data else b'[empty]\n')
                sys.stdout.buffer.flush()
            else:
                print(data)

    async def healthcheck(self, slug):
        '''Performs an healthcheck using MKCTFAPI
        '''
        async for report in self._api.healthcheck(slug, timeout=self._task_timeout):
            yield report

    async def post(self, slug, healthy):
        '''Post a healthcheck report to the scoreboard
        '''
        async with ClientSession(auth=self._auth, timeout=self._post_timeout) as session:
            app_log.info(f"posting {slug} report to {self._url}...")
            async with session.post(self._url, ssl=self._ssl, json={slug: healthy}) as resp:
                if resp.status < 400:
                    app_log.info("post succeeded.")
                else:
                    app_log.error("post failed.")

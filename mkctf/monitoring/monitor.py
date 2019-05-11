# =============================================================================
#  IMPORTS
# =============================================================================
import sys
from time import time
from asyncio import (
    CancelledError,
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
        # get next task out of the queue
        task = await monitor.task_queue.get()
        if task is None:
            await monitor.print(f"[{worker_id}]: exiting gracefully")
            break
        # process task
        await monitor.print(f"[{worker_id}]: waiting for {task.slug} to reach schedule: {naturaldelta(task.countdown)} remaining")
        await task.is_ready()
        await monitor.print(f"[{worker_id}]: running healthcheck for {task.slug}")
        try:
            report = await task.run()
        except Exception as exc:
            report = None
            await monitor.post(worker_id, task.slug, False)
            await monitor.print(f"[{worker_id}]: an exception occured while running healthcheck for {task.slug}: {exc}")
        else:
            await monitor.post(worker_id, task.slug, report['healthy'])
        # inject exploit back in queue if needed
        if task.should_run_again:
            await monitor.task_queue.put(task)
        # notify the queue that the task has been processed
        monitor.task_queue.task_done()
        # print report
        if report:
            stdout = b''
            stderr = b''
            health = 'healthy' if report['healthy'] else 'DEAD'
            sep = ('=' * 80) + '\n'
            text = sep
            text += f"[{worker_id}]: reporting for {task.slug}\n"
            text += f"[{worker_id}]:  - state: {health}\n"
            text += f"[{worker_id}]:  - check duration: {naturaldelta(task.duration)}\n"
            if not report['healthy']:
                stdout = f"----------------[{task.slug}:STDOUT]----------------\n"
                stdout = stdout.encode() + report['stdout']
                stderr = f"----------------[{task.slug}:STDERR]----------------\n"
                stderr = stderr.encode() + report['stderr']
            text = text.encode() + stdout + stderr + sep.encode()
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
        self._post_timeout = ClientTimeout(total=post_timeout)

    @property
    def task_queue(self):
        return self._task_queue

    @property
    def iter_cnt(self):
        return self._iter_cnt

    @property
    def iter_delay(self):
        return self._iter_delay

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
        async for report in self._api.healthcheck(slug=slug, timeout=self._task_timeout):
            yield report

    async def post(self, caller_id, slug, healthy):
        '''Post a healthcheck report to the scoreboard
        '''
        try:
            async with ClientSession(auth=self._auth, timeout=self._post_timeout) as session:
                await self.print(f"[{caller_id}]: posting {slug} report to {self._url}...")
                async with session.post(self._url, ssl=self._ssl, json={slug: healthy}) as resp:
                    if resp.status < 400:
                        await self.print(f"[{caller_id}]: post succeeded.")
                    else:
                        await self.print(f"[{caller_id}]: post failed.")
        except Exception as exc:
            await self.print(f"[{caller_id}]: an execption occured while contacting the scoreboard: {exc}")

    async def run(self):
        '''[summary]
        '''
        for challenge in self._api.enum():
            if not challenge['conf']['enabled']:
                await self.print(f"[monitor]: {challenge['slug']} skipped (disabled)")
                continue
            await self.print(f"[monitor]: injecting a task for {challenge['slug']}...")
            await self._task_queue.put(MonitorTask(self, challenge['slug']))
        # check if queue is empty before starting
        if self._task_queue.empty():
            await self.print(f"[monitor]: no task to process, exiting.")
            return
        # create 4 worker tasks to process the queue concurrently
        await self.print(f"[monitor]: spawning {self._worker_cnt} workers...")
        for k in range(self._worker_cnt):
            worker = create_task(worker_routine(f'worker-{k}', self))
            self._workers.append(worker)
        # await queue to be processed entirely
        await self.print(f"[monitor]: waiting for tasks to be processed...")
        try:
            await self._task_queue.join()
        except CancelledError:
            await self.print("[monitor]: tasks cancelled.")
        # terminate workers
        await self.print(f"[monitor]: terminating workers...")
        for _ in self._workers:
            await self._task_queue.put(None)
        # await workers termination
        await self.print(f"[monitor]: waiting for workers to terminate...")
        await gather(*self._workers, return_exceptions=True)
        await self.print(f"[monitor]: exiting.")

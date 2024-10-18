"""mkctf monitor implementation
"""

from dataclasses import dataclass
from time import time

from ..api import MKCTFAPI
from ..helper.display import display_cpr
from ..helper.subprocess import CalledProcessResult


@dataclass
class MonitorTask:
    """Monitor task"""

    mkctf_api: MKCTFAPI
    slug: str
    timeout: int
    beg: int = 0
    end: int = 0
    count: int = 0

    @property
    def duration(self) -> int:
        """Task duration"""
        return self.end - self.beg

    def countdown(self, delay: int) -> int:
        """Remaining time until next run"""
        return delay - (int(time()) - self.beg)

    async def run(self) -> CalledProcessResult:
        """Run the task"""
        self.beg = int(time())
        self.count += 1
        result = None
        async for _, cpr in self.mkctf_api.healthcheck(
            slug=self.slug, timeout=self.timeout
        ):
            result = cpr
        self.end = int(time())
        if result:
            display_cpr(self.slug, result)
        return result

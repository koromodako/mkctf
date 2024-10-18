"""Monitor notifier implementation
"""

from dataclasses import dataclass

from aiohttp import BasicAuth, ClientSession, ClientTimeout
from yarl import URL

from ..helper.logging import LOGGER


@dataclass
class MonitorNotifier:
    """Monitor notifier"""

    base_url: URL
    username: str
    password: str
    timeout: int = 60
    ssl: bool = True

    async def post(self, worker_id: str, slug: str, healthy: bool):
        """Post a healthcheck report to the dashboard API"""
        auth = BasicAuth(self.username, self.password)
        timeout = ClientTimeout(total=self.timeout)
        url = self.base_url.with_path('/mkctf-api/healthcheck')
        LOGGER.info("[%s]: posting %s report to %s", worker_id, slug, url)
        async with ClientSession(auth=auth, timeout=timeout) as session:
            try:
                async with session.post(
                    url, ssl=self.ssl, json={slug: healthy}
                ) as resp:
                    if resp.status < 400:
                        LOGGER.info("[%s]: post succeeded.", worker_id)
                    else:
                        LOGGER.warning("[%s]: post failed.", worker_id)
            except Exception as exc:
                LOGGER.error(
                    "[%s]: failed to post to the dashboard API: %s",
                    worker_id,
                    exc,
                )

from aiohttp.web import Response
import asyncio
from dataclasses import dataclass, field
from datetime import timedelta
import logging
from typing import List

from .callbacks import terminate_on_error
from .apisession import Retry


logger = logging.getLogger(__name__)


@dataclass
class Debouncer:
    interval: timedelta
    statuses: List[int]
    _condition: asyncio.Condition = field(init=False, default=None)
    _task: asyncio.Task = field(init=False, default=None)
    _backing_off: bool = field(init=False, default=False)

    def set_apisession(self, apisession):
        if not self._task:
            self._task = asyncio.create_task(self.run())
            self._task.add_done_callback(terminate_on_error)

    async def handle_response(self, response: Response) -> Response:
        if self._condition and response.status in self.statuses:
            async with self._condition:
                logger.info(f'Response [{response.status}]')
                self._condition.notify()
            return Retry
        return response

    def backing_off(self) -> bool:
        return self._backing_off

    async def run(self):
        self._condition = asyncio.Condition()
        interval_secs = self.interval.total_seconds()

        logger.info('Starting Debouncer')
        while True:
            async with self._condition:
                self._backing_off = False
                await self._condition.wait()
                logger.info(f'Debounce - wait for {interval_secs} seconds')
                self._backing_off = True
                await asyncio.sleep(interval_secs)

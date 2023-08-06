import time

from typing import Tuple, Dict
from loguru import logger

from .worker import Worker
from .ticket import Ticket


class EchoWorker(Worker):
    def __init__(self) -> None:
        super(EchoWorker, self).__init__()
        self.busy = False

    @property
    def name(self) -> str:
        return "echo-worker"

    @property
    def duties(self) -> Tuple:
        return ("echo",)

    @property
    def is_busy(self) -> bool:
        return self.busy

    @property
    def status(self) -> Dict:
        return {}

    def setup(self) -> None:
        logger.info("setup")

    def teardown(self) -> None:
        logger.info("teardown")

    def doing(self, ticket: Ticket) -> Ticket:
        logger.info("start work")
        time.sleep(0.1)
        logger.info("finish work")
        return ticket

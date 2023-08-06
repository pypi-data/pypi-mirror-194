from typing import List, Union
from concurrent.futures import ProcessPoolExecutor, TimeoutError

from .errors import YumNotImplemented, YumUnavailable, YumTimeout
from .ticket import Ticket
from .worker import Worker


def _handle(worker: Worker, ticket: Ticket) -> Union[Ticket, None]:
    with worker as w:
        return w.doing(ticket)


class Manager(object):
    executor = ProcessPoolExecutor()

    def __init__(self) -> None:
        self.workers: List[Worker] = []

    def hire(self, worker: Worker) -> None:
        wokers_id = [k.id for k in self.workers]
        if worker.id not in wokers_id:
            self.workers.append(worker)

    def capable(self, duty: str) -> Worker:
        capable_list = [w for w in self.workers if (duty in w.duties)]

        if len(capable_list) < 1:
            raise YumNotImplemented

        result = capable_list[0]
        if result.busy:
            raise YumUnavailable

        return result

    def perform(self, ticket: Ticket, timeout: int = 15) -> Union[Ticket, None]:
        worker = self.capable(ticket.code)

        fr = Manager.executor.submit(_handle, worker, ticket)
        try:
            return fr.result(timeout)
        except TimeoutError:
            raise YumTimeout

    def off_duty(self):
        Manager.executor.shutdown()

from preemo.worker._env import get_optional_env as _get_optional_env
from preemo.worker._messaging_client import IMessagingClient as _IMessagingClient
from preemo.worker._messaging_client import (
    LocalMessagingClient as _LocalMessagingClient,
)
from preemo.worker._messaging_client import MessagingClient as _MessagingClient
from preemo.worker._worker_client import WorkerClient as _WorkerClient

__all__ = ["register"]


def _construct_messaging_client() -> _IMessagingClient:
    worker_server_url = _get_optional_env("PREEMO_WORKER_SERVER_URL")

    if worker_server_url is None:
        return _LocalMessagingClient()

    return _MessagingClient(worker_server_url=worker_server_url)


_worker_client = _WorkerClient(messaging_client=_construct_messaging_client())

register = _worker_client.register

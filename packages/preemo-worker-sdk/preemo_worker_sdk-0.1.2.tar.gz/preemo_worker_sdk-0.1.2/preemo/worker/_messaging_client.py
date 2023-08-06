from typing import Protocol, runtime_checkable

import zmq

from preemo import __version__
from preemo.gen.header_pb2 import HeaderReply, HeaderRequest
from preemo.gen.shared.status_pb2 import STATUS_OK
from preemo.gen.worker.reply_pb2 import RegisterFunctionReply, WorkerReply
from preemo.gen.worker.request_pb2 import WorkerRequest


@runtime_checkable
class IMessagingClient(Protocol):
    def send_worker_request(self, worker_request: WorkerRequest) -> WorkerReply:
        pass


# Instantiating this class will hang if it cannot connect to a valid server
class MessagingClient:
    def __init__(self, *, worker_server_url: str) -> None:
        context = zmq.Context()

        # TODO(adrian@preemo.io, 02/25/2023): investigate other socket types, such as PUSH/PULL
        self._socket = context.socket(zmq.REQ)
        # TODO(adrian@preemo.io, 02/15/2023): add logging indicating attempting to connect and successful connection
        # TODO(adrian@preemo.io, 02/15/2023): add timeout, like Promise.race (python threads)
        # TODO(adrian@preemo.io, 02/16/2023): investigate which, if any of these timeouts are useful
        # self._socket.setsockopt(zmq.CONNECT_TIMEOUT, 1_000)
        # self._socket.setsockopt(zmq.SNDTIMEO, 1_000)
        # self._socket.setsockopt(zmq.RCVTIMEO, 1_000)
        self._socket.connect(worker_server_url)

        header_reply = self._send_header_request(HeaderRequest(version=__version__))
        if header_reply.status != STATUS_OK:
            raise Exception(
                f"worker server replied to header request with unexpected status: {header_reply.status} and message: {header_reply.message}"
            )

    def _send_message(self, message: bytes) -> bytes:
        self._socket.send(message)
        return self._socket.recv()

    def _send_header_request(self, header_request: HeaderRequest) -> HeaderReply:
        message = header_request.SerializeToString()
        reply = self._send_message(message)

        return HeaderReply.FromString(reply)

    def send_worker_request(self, worker_request: WorkerRequest) -> WorkerReply:
        message = worker_request.SerializeToString()
        reply = self._send_message(message)

        return WorkerReply.FromString(reply)


# This class is intended to be used for tests and local development
class LocalMessagingClient:
    def send_worker_request(self, worker_request: WorkerRequest) -> WorkerReply:
        print(f"sending worker request: {worker_request}")
        # TODO(adrian@preemo.io, 02/15/2023): have this send a different reply for different request types
        return WorkerReply(register_function=RegisterFunctionReply(status=STATUS_OK))

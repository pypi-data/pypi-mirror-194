from shared import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterFunctionReply(_message.Message):
    __slots__ = ["message", "status"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    message: str
    status: _status_pb2.Status
    def __init__(self, status: _Optional[_Union[_status_pb2.Status, str]] = ..., message: _Optional[str] = ...) -> None: ...

class WorkerReply(_message.Message):
    __slots__ = ["register_function"]
    REGISTER_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    register_function: RegisterFunctionReply
    def __init__(self, register_function: _Optional[_Union[RegisterFunctionReply, _Mapping]] = ...) -> None: ...

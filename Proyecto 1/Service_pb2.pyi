from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class File(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    def __init__(self, content: _Optional[bytes] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("requestFile",)
    REQUESTFILE_FIELD_NUMBER: _ClassVar[int]
    requestFile: str
    def __init__(self, requestFile: _Optional[str] = ...) -> None: ...

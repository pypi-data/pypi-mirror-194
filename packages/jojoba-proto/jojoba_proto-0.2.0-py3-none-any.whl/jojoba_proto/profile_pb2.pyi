from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePositionRequest(_message.Message):
    __slots__ = ["editable", "employer_key"]
    EDITABLE_FIELD_NUMBER: _ClassVar[int]
    EMPLOYER_KEY_FIELD_NUMBER: _ClassVar[int]
    editable: PositionsEditable
    employer_key: ProfileKey
    def __init__(self, employer_key: _Optional[_Union[ProfileKey, _Mapping]] = ..., editable: _Optional[_Union[PositionsEditable, _Mapping]] = ...) -> None: ...

class Employee(_message.Message):
    __slots__ = ["editable", "key"]
    EDITABLE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    editable: EmployeeEditable
    key: ProfileKey
    def __init__(self, key: _Optional[_Union[ProfileKey, _Mapping]] = ..., editable: _Optional[_Union[EmployeeEditable, _Mapping]] = ...) -> None: ...

class EmployeeEditable(_message.Message):
    __slots__ = ["desc", "name"]
    DESC_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    desc: str
    name: str
    def __init__(self, name: _Optional[str] = ..., desc: _Optional[str] = ...) -> None: ...

class Employer(_message.Message):
    __slots__ = ["editable", "key"]
    EDITABLE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    editable: EmployerEditable
    key: ProfileKey
    def __init__(self, key: _Optional[_Union[ProfileKey, _Mapping]] = ..., editable: _Optional[_Union[EmployerEditable, _Mapping]] = ...) -> None: ...

class EmployerEditable(_message.Message):
    __slots__ = ["desc", "name"]
    DESC_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    desc: str
    name: str
    def __init__(self, name: _Optional[str] = ..., desc: _Optional[str] = ...) -> None: ...

class GetProfileResponse(_message.Message):
    __slots__ = ["employee", "employer", "neither"]
    EMPLOYEE_FIELD_NUMBER: _ClassVar[int]
    EMPLOYER_FIELD_NUMBER: _ClassVar[int]
    NEITHER_FIELD_NUMBER: _ClassVar[int]
    employee: Employee
    employer: Employer
    neither: _empty_pb2.Empty
    def __init__(self, employee: _Optional[_Union[Employee, _Mapping]] = ..., employer: _Optional[_Union[Employer, _Mapping]] = ..., neither: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class Position(_message.Message):
    __slots__ = ["editable", "key"]
    EDITABLE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    editable: PositionsEditable
    key: PositionKey
    def __init__(self, key: _Optional[_Union[PositionKey, _Mapping]] = ..., editable: _Optional[_Union[PositionsEditable, _Mapping]] = ...) -> None: ...

class PositionKey(_message.Message):
    __slots__ = ["position_id", "user_id"]
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    position_id: int
    user_id: int
    def __init__(self, user_id: _Optional[int] = ..., position_id: _Optional[int] = ...) -> None: ...

class PositionsEditable(_message.Message):
    __slots__ = ["desc", "title"]
    DESC_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    desc: str
    title: str
    def __init__(self, title: _Optional[str] = ..., desc: _Optional[str] = ...) -> None: ...

class ProfileKey(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

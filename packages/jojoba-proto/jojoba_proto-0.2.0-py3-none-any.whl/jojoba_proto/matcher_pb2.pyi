from google.protobuf import empty_pb2 as _empty_pb2
import profile_pb2 as _profile_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DISLIKE: SwipeActionType
LIKE: SwipeActionType

class EmployeeMatch(_message.Message):
    __slots__ = ["created_ts", "employee_key", "position_match_key"]
    CREATED_TS_FIELD_NUMBER: _ClassVar[int]
    EMPLOYEE_KEY_FIELD_NUMBER: _ClassVar[int]
    POSITION_MATCH_KEY_FIELD_NUMBER: _ClassVar[int]
    created_ts: int
    employee_key: _profile_pb2.ProfileKey
    position_match_key: _profile_pb2.PositionKey
    def __init__(self, employee_key: _Optional[_Union[_profile_pb2.ProfileKey, _Mapping]] = ..., position_match_key: _Optional[_Union[_profile_pb2.PositionKey, _Mapping]] = ..., created_ts: _Optional[int] = ...) -> None: ...

class EmployeeSwipeAction(_message.Message):
    __slots__ = ["employee_sender_key", "position_receiver_key", "type"]
    EMPLOYEE_SENDER_KEY_FIELD_NUMBER: _ClassVar[int]
    POSITION_RECEIVER_KEY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    employee_sender_key: _profile_pb2.ProfileKey
    position_receiver_key: _profile_pb2.PositionKey
    type: SwipeActionType
    def __init__(self, employee_sender_key: _Optional[_Union[_profile_pb2.ProfileKey, _Mapping]] = ..., position_receiver_key: _Optional[_Union[_profile_pb2.PositionKey, _Mapping]] = ..., type: _Optional[_Union[SwipeActionType, str]] = ...) -> None: ...

class GetEmployeeMatchesRequest(_message.Message):
    __slots__ = ["employee_key", "pagination"]
    EMPLOYEE_KEY_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    employee_key: _profile_pb2.ProfileKey
    pagination: Pagination
    def __init__(self, employee_key: _Optional[_Union[_profile_pb2.ProfileKey, _Mapping]] = ..., pagination: _Optional[_Union[Pagination, _Mapping]] = ...) -> None: ...

class GetPositionMatchesRequest(_message.Message):
    __slots__ = ["pagination", "position_key"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    POSITION_KEY_FIELD_NUMBER: _ClassVar[int]
    pagination: Pagination
    position_key: _profile_pb2.PositionKey
    def __init__(self, position_key: _Optional[_Union[_profile_pb2.PositionKey, _Mapping]] = ..., pagination: _Optional[_Union[Pagination, _Mapping]] = ...) -> None: ...

class Pagination(_message.Message):
    __slots__ = ["limit", "offset"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    def __init__(self, limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class PositionMatch(_message.Message):
    __slots__ = ["created_ts", "employee_match_key", "position_key"]
    CREATED_TS_FIELD_NUMBER: _ClassVar[int]
    EMPLOYEE_MATCH_KEY_FIELD_NUMBER: _ClassVar[int]
    POSITION_KEY_FIELD_NUMBER: _ClassVar[int]
    created_ts: int
    employee_match_key: _profile_pb2.ProfileKey
    position_key: _profile_pb2.PositionKey
    def __init__(self, position_key: _Optional[_Union[_profile_pb2.PositionKey, _Mapping]] = ..., employee_match_key: _Optional[_Union[_profile_pb2.ProfileKey, _Mapping]] = ..., created_ts: _Optional[int] = ...) -> None: ...

class PositionSwipeAction(_message.Message):
    __slots__ = ["employee_receiver_key", "position_sender_key", "type"]
    EMPLOYEE_RECEIVER_KEY_FIELD_NUMBER: _ClassVar[int]
    POSITION_SENDER_KEY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    employee_receiver_key: _profile_pb2.ProfileKey
    position_sender_key: _profile_pb2.PositionKey
    type: SwipeActionType
    def __init__(self, position_sender_key: _Optional[_Union[_profile_pb2.PositionKey, _Mapping]] = ..., employee_receiver_key: _Optional[_Union[_profile_pb2.ProfileKey, _Mapping]] = ..., type: _Optional[_Union[SwipeActionType, str]] = ...) -> None: ...

class SwipeActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

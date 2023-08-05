from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthorizeRequest(_message.Message):
    __slots__ = ["body", "method"]
    BODY_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    body: _any_pb2.Any
    method: str
    def __init__(self, method: _Optional[str] = ..., body: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class IssueTokenRequest(_message.Message):
    __slots__ = ["ropc"]
    ROPC_FIELD_NUMBER: _ClassVar[int]
    ropc: ROPCAuthorizationGrant
    def __init__(self, ropc: _Optional[_Union[ROPCAuthorizationGrant, _Mapping]] = ...) -> None: ...

class IssueTokenResponse(_message.Message):
    __slots__ = ["access_token", "token_type"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    token_type: str
    def __init__(self, access_token: _Optional[str] = ..., token_type: _Optional[str] = ...) -> None: ...

class ROPCAuthorizationGrant(_message.Message):
    __slots__ = ["user_email", "user_password"]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    user_email: str
    user_password: str
    def __init__(self, user_email: _Optional[str] = ..., user_password: _Optional[str] = ...) -> None: ...

class RegisterRequest(_message.Message):
    __slots__ = ["user_email", "user_password"]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    user_email: str
    user_password: str
    def __init__(self, user_email: _Optional[str] = ..., user_password: _Optional[str] = ...) -> None: ...

class RevokeTokenRequest(_message.Message):
    __slots__ = ["token"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["email", "id", "login"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    email: str
    id: int
    login: str
    def __init__(self, id: _Optional[int] = ..., login: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

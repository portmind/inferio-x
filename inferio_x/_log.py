import datetime
from typing import Any, Dict, Optional, TypedDict, Union


class SuccessData(TypedDict):
    request: Dict[str, Any]
    response: Dict[str, Any]
    timestamp: datetime.datetime
    duration_ms: float
    ip: Optional[str]
    status_code: int


class FailData(TypedDict):
    body: Optional[Dict[str, Any]]
    timestamp: datetime.datetime
    ip: Optional[str]
    status_code: int


class Log(TypedDict):
    app: str
    path: str
    data: Union[FailData, SuccessData]

from datetime import datetime
from typing import Optional

from starlette.background import BackgroundTask
from starlette.requests import Request

from inferio_x._background import send_log
from inferio_x._log import FailData, Log


def create_background_task_for_exception(
    request: Request, status_code: int
) -> Optional[BackgroundTask]:
    background = None
    has_logging = False
    try:
        has_logging = request.state.has_logging
    except AttributeError:
        pass
    if has_logging:
        try:
            body = request.state.payload
        except AttributeError:
            body = None
        ip = None
        if request.client:
            ip = f"{request.client.host}:{request.client.port}"
        data = FailData(
            body=body,
            timestamp=datetime.now(),
            ip=ip,
            status_code=status_code,
        )
        log = Log(
            app=request.app.state.APP_NAME,
            path=request.scope["path"],
            data=data,
        )
        background = BackgroundTask(send_log, log)
    return background

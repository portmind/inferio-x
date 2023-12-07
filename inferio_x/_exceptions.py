import pydantic
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from inferio_x._response import OrJSONResponse
from inferio_x._utils import create_background_task_for_exception


async def http_exception(_: Request, exc: HTTPException):
    return OrJSONResponse(
        content={"error": exc.detail},
        status_code=exc.status_code,
        headers=exc.headers,
    )


async def bad_request(request: Request, exc: pydantic.ValidationError):
    status_code = HTTP_400_BAD_REQUEST
    background = create_background_task_for_exception(
        request, status_code=status_code
    )
    return OrJSONResponse(
        content={"error": exc.errors()},
        status_code=status_code,
        background=background,
    )


def server_error(request: Request, exc: HTTPException):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    background = create_background_task_for_exception(
        request, status_code=status_code
    )
    return OrJSONResponse(
        content={"error": str(exc)},
        status_code=status_code,
        background=background,
    )


exception_handlers = {
    HTTPException: http_exception,
    pydantic.ValidationError: bad_request,
    Exception: server_error,
}

import json
import time
from asyncio import iscoroutinefunction
from datetime import datetime
from functools import wraps
from typing import Any, Callable, List, Optional, Type, get_type_hints

import uvicorn
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.datastructures import UploadFile as StarletteUploadFile
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.status import HTTP_200_OK
from starlette_exporter import PrometheusMiddleware, handle_metrics

from inferio_x._background import send_log
from inferio_x._configs import INFERIO_APP_NAME, TIMEOUT_KEEP_ALIVE
from inferio_x._endpoint import Endpoint
from inferio_x._exceptions import exception_handlers
from inferio_x._file import FileUpload
from inferio_x._log import Log, SuccessData
from inferio_x._method import Method
from inferio_x._response import OrJSONResponse


class Service:

    __slots__ = (
        "app",
        "port",
        "access_log",
        "endpoints",
        "debug",
        "host",
        "name",
    )

    def __init__(
        self,
        endpoints: List[Endpoint],
        name: str = INFERIO_APP_NAME,
        host: str = "0.0.0.0",
        port: int = 8081,
        debug: bool = False,
        access_log: bool = True,
    ) -> None:
        middlewares = [
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
        self.endpoints = endpoints
        self.host = host
        self.port = port
        self.access_log = access_log
        self.app = Starlette(
            debug=debug,
            middleware=middlewares,
            exception_handlers=exception_handlers,
        )
        self.app.state.APP_NAME = name
        self._post_init()

    def _post_init(self) -> None:
        skip_paths = []
        for endpoint in self.endpoints:
            if not endpoint.monitor:
                skip_paths.append(endpoint.path)
            handler_type_hints = get_type_hints(endpoint.handler)
            payload_type = handler_type_hints.get("payload")
            if payload_type is not None:
                if issubclass(payload_type, BaseModel):
                    validator = payload_type
                else:
                    validator = None
            else:
                validator = None

            decorated_handler = self.call_wrapper(
                handler=endpoint.handler,
                logger=endpoint.logger,
                path=endpoint.path,
                validator=validator,
            )
            self.app.add_route(
                endpoint.path,
                decorated_handler,
                methods=[m.value for m in endpoint.methods],
            )
        self.app.add_middleware(
            PrometheusMiddleware,
            skip_paths=skip_paths,
            app_name=self.app.state.APP_NAME,
        )
        self.app.add_route("/metrics", handle_metrics)

    def call_wrapper(
        self,
        handler: Callable,
        logger: bool,
        path: str,
        validator: Optional[Type[BaseModel]],
    ) -> Callable:
        is_fn_coroutine = iscoroutinefunction(handler)

        @wraps(handler)
        async def wrapper(request: Request) -> Any:
            request.state.has_logging = logger
            payload = None
            try:
                # Try to process request as json
                payload = await request.json()
            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                # Try to process request as form data
                if request.method == Method.POST.value:
                    form = await request.form()
                    if form:
                        payload = dict()
                        for name, value in form.items():
                            payload[name] = (
                                await FileUpload.create(value)
                                if isinstance(value, StarletteUploadFile)
                                else value
                            )
            except BaseException:
                pass

            if (payload is None) and (request.query_params):
                payload = {
                    key: val for key, val in request.query_params.items()
                }
            request.state.payload = payload
            background = None
            if payload:
                if validator:
                    validated_payload = validator(**payload)
                else:
                    validated_payload = payload
                request.state.time_started = time.perf_counter()
                response = (
                    await handler(validated_payload)
                    if is_fn_coroutine
                    else handler(validated_payload)
                )
                request.state.time_ended = time.perf_counter()
                if logger:
                    duration_ms = round(
                        request.state.time_ended - request.state.time_started,
                        2,
                    )
                    ip = (
                        f"{request.client.host}:{request.client.port}"
                        if request.client
                        else None
                    )
                    data = SuccessData(
                        request=payload,
                        response=response,
                        timestamp=datetime.now(),
                        duration_ms=duration_ms,
                        ip=ip,
                        status_code=HTTP_200_OK,
                    )
                    log = Log(
                        app=self.app.state.APP_NAME, path=path, data=data
                    )
                    background = BackgroundTask(send_log, log)
            else:
                response = await handler() if is_fn_coroutine else handler()
            return OrJSONResponse(response, background=background)

        return wrapper

    def run(self) -> None:
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            access_log=self.access_log,
            log_level="info",
            use_colors=False,
            timeout_keep_alive=TIMEOUT_KEEP_ALIVE
        )

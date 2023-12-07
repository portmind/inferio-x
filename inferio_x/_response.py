from typing import Any

import orjson
from starlette.responses import JSONResponse


class OrJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY)

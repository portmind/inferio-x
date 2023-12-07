import httpx
import orjson

from inferio_x._configs import YAMLLOG_PASS, YAMLLOG_URL, YAMLLOG_USER
from inferio_x._log import Log


async def send_log(log: Log) -> None:
    try:
        async with httpx.AsyncClient() as client:
            _ = await client.post(
                YAMLLOG_URL,
                content=orjson.dumps(log, option=orjson.OPT_SERIALIZE_NUMPY),
                auth=(YAMLLOG_USER, YAMLLOG_PASS),
            )
    except httpx.HTTPError as err:
        # TODO: replace print with logging module
        print(f"Error while sending logs to Elastic {err.request.url!r}.")

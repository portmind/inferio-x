from starlette.config import Config

config = Config(".env")

YAMLLOG_URL = config("YAMLLOG_URL", default="")
YAMLLOG_USER = config("YAMLLOG_USER", default="")
YAMLLOG_PASS = config("YAMLLOG_PASS", default="")
INFERIO_APP_NAME = config("INFERIO_APP_NAME", default="serveml")

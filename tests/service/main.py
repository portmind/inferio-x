from service.config import config
from service.predictor import Predictor

from inferio_x import Endpoint, Method, Service

predictor = Predictor(config)

service = Service(
    name="serveml",
    endpoints=[
        Endpoint(
            "/path",
            handler=predictor.predict,
            monitor=True,
            methods=[Method.POST],
        )
    ],
    debug=True,
)

if __name__ == "__main__":
    service.run()

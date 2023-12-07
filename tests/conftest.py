import functools

import pytest
from service.config import config
from service.predictor import Predictor
from starlette.testclient import TestClient

from inferio_x import Endpoint, Method, Service


@pytest.fixture
def predictor():
    return Predictor(config)


@pytest.fixture
def service(predictor):
    service = Service(
        endpoints=[
            Endpoint(
                path="/",
                handler=predictor.predict,
                methods=[Method.POST],
            ),
            Endpoint(
                path="/predict",
                handler=predictor.predict,
                methods=[Method.POST],
                logger=True,
            ),
            Endpoint(
                path="/inference-results",
                handler=predictor.get_inference_results,
                methods=[Method.GET, Method.POST],
            ),
            Endpoint(
                path="/predict-by-error",
                handler=predictor.predict_by_error,
                methods=[Method.POST],
            ),
            Endpoint(
                path="/predict-async",
                handler=predictor.predict_async,
                methods=[Method.POST],
            ),
            Endpoint(
                path="/inference-results-async",
                handler=predictor.get_inference_results_async,
                methods=[Method.GET, Method.POST],
            ),
            Endpoint(
                path="/predict-by-query",
                handler=predictor.predict_by_query,
                methods=[Method.GET, Method.POST],
                monitor=False,
            ),
            Endpoint(
                path="/predict-by-form-data",
                handler=predictor.predict_by_form_data,
                methods=[Method.POST],
                monitor=False,
            ),
        ],
        debug=False,
    )
    return service


@pytest.fixture
def test_client_factory():
    return functools.partial(
        TestClient,
        backend_options={"use_uvloop": True},
        raise_server_exceptions=False,
    )


@pytest.fixture
def client(test_client_factory, service):
    with test_client_factory(service.app) as client:
        yield client

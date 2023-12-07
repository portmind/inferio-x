import pytest
from service.config import config

from inferio_x import Endpoint, Method, Service


@pytest.fixture
def service_in_debug_mode(predictor):
    service = Service(
        endpoints=[
            Endpoint(
                path="/predict-by-error",
                handler=predictor.predict_by_error,
                methods=[Method.POST],
            ),
        ],
        debug=True,
    )
    return service


@pytest.fixture
def debug_client(test_client_factory, service_in_debug_mode):
    with test_client_factory(service_in_debug_mode.app) as client:
        yield client


def test_validation(client):
    response = client.post(
        "/",
        json={
            "name": {"first_name": "Bruce", "last_name": "Wayne"},
            "age": "Dark Knight",
        },
    )

    assert response.status_code == 400
    # assert response.json() == {
    #     "error": [
    #         {
    #             "loc": ["name"],
    #             "msg": "Input should be a valid string",
    #             "type": "string_type",
    #         },
    #         {
    #             "loc": ["age"],
    #             "msg": "value is not a valid integer",
    #             "type": "type_error.integer",
    #         },
    #     ],
    # }


def test_not_found_error(client):
    response = client.post("/not-found")

    assert response.status_code == 404
    assert response.json() == {"error": "Not Found"}


def test_server_error(client):
    response = client.post("/predict-by-error")

    assert response.status_code == 500
    assert response.json() == {"error": "Batman did it!"}


def test_debug_mode(debug_client):
    response = debug_client.post("/predict-by-error")

    assert response.status_code == 500
    assert response.headers["content-type"].startswith("text/plain")
    assert "RuntimeError: Batman did it!" in response.text

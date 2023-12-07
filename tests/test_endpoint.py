import pytest

from inferio_x import Endpoint, Method


def test_endpoint_starting_with_slash(predictor):
    with pytest.raises(ValueError, match="Routed paths must start with '/'"):
        Endpoint(
            path="predict", handler=predictor.predict, methods=[Method.POST]
        )


def test_endpoint_with_empty_methods(predictor):
    with pytest.raises(
        ValueError, match="Methods must include at least one HTTP method"
    ):
        Endpoint(path="/predict", handler=predictor.predict, methods=[])

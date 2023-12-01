import os

import pytest


@pytest.mark.parametrize("path", ["/", "/predict"])
def test_predict_path(client, path):
    response = client.post(path, json={"name": "John", "age": 21})

    assert response.status_code == 200
    assert response.json() == {"name": "John", "age": 21, "accepted": True}


def test_predict_async(client):
    response = client.post("/predict-async", json={"name": "John", "age": 21})

    assert response.status_code == 200
    assert response.json() == {"name": "John", "age": 21, "accepted": True}


@pytest.mark.parametrize("method", ["get", "post"])
def test_get_inference_results_path(client, method):
    method_func = getattr(client, method)

    response = method_func("/inference-results")

    assert response.status_code == 200
    assert response.json() == {
        "prediction": 0.7,
        "scores": [[0.012, None], [0.2001, 0.107]],
    }


@pytest.mark.parametrize("method", ["get", "post"])
def test_get_inference_results_async_path(client, method):
    method_func = getattr(client, method)

    response = method_func("/inference-results-async")

    assert response.status_code == 200
    assert response.json() == {
        "prediction": 0.7,
        "scores": [[0.012, None], [0.2001, 0.107]],
    }


def test_get_predict_by_query_path(client):
    response = client.get("/predict-by-query?id=4")
    assert response.status_code == 200
    assert response.json() == {"response": "4"}


def test_predict_by_form_data(client):
    here = os.path.abspath(os.path.dirname(__file__))
    test_file = os.path.join(here, "static", "example.pdf")
    with open(test_file, "rb") as f:
        response = client.post(
            "/predict-by-form-data",
            data={"name": "John", "age": 21},
            files={"document": f},
        )

    assert response.status_code == 200
    assert response.json() == {"response": "example.pdf, application/pdf, pdf"}


def test_metrics(client):
    test_get_predict_by_query_path(client)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "predict-by-query" not in response.text

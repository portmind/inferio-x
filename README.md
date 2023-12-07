# InferIO-X

Inference I/O Extended

![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-brightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)



## Installation
```shell
$ pip install inferio-x==0.1.0
```

## Usage
```python
from pydantic import BaseModel
from inferio import Service, Endpoint, Method


class PredictPayload(BaseModel):
    name: str
    age: int


class Predictor:
    def __init__(self, model_f: str) -> None:
        self.model_f = model_f

    def predict(self, payload: PredictPayload) -> dict: ...


if __name__ == "__main__":
    predictor = Predictor(model_f="model.pth")
    service = Service(
    endpoints=[
        Endpoint(path="/", handler=predictor.predict, methods=[Method.POST]),
    ])
    service.run()

```

## Tests

To run the tests, use the following command:

```shell
$ poetry run pytest
```

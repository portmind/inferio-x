class Pipeline:
    def __init__(self) -> None:
        pass

    def predict(self, name: str, age: int) -> dict:
        return {
            "name": name,
            "age": age,
            "accepted": True,
        }

    def get_inference_results(self) -> dict:
        return {
            "prediction": 0.7,
            "scores": [[0.012, None], [0.2001, 0.107]],
        }

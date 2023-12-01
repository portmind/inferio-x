import asyncio
from typing import Dict, Optional

import pydantic
from inferio import FileUpload

from .pipeline import Pipeline


class PredictPayload(pydantic.BaseModel):
    name: str
    age: int
    document: Optional[FileUpload] = None


class Predictor:
    def __init__(self, config: Dict[str, str]) -> None:
        self.model_file = config["model_file"]
        self.pipeline = Pipeline()

    def predict(self, payload: PredictPayload):
        return self.pipeline.predict(payload.name, payload.age)

    async def predict_async(self, payload: PredictPayload):
        await asyncio.sleep(1)
        return self.pipeline.predict(payload.name, payload.age)

    def get_inference_results(self) -> dict:
        return self.pipeline.get_inference_results()

    async def get_inference_results_async(self) -> dict:
        await asyncio.sleep(1)
        return self.pipeline.get_inference_results()

    def predict_by_error(self):
        raise RuntimeError("Batman did it!")

    def predict_by_query(self, request: Dict[str, str]):
        return {"response": request["id"]}

    def predict_by_form_data(self, payload: PredictPayload):
        doc = payload.document
        if doc:
            format = doc.file[1:4].decode().lower()
            response = {
                "response": f"{doc.filename}, {doc.content_type}, {format}"
            }

            return response
        

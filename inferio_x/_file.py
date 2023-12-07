from pydantic import BaseModel
from starlette.datastructures import UploadFile as StarletteUploadFile


class FileUpload(BaseModel):
    file: bytes
    filename: str
    content_type: str

    @classmethod
    async def create(cls, file: StarletteUploadFile):
        data = await file.read()

        return cls(
            file=data,
            filename=file.filename, # type: ignore
            content_type=file.content_type, # type: ignore
        )

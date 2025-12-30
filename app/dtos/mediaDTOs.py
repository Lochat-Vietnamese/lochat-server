import os
from typing import List
from uuid import UUID
from pydantic import Field, field_validator
from app.enums.responseMessages import ResponseMessages
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.parseBool import ParseBool
from app.dtos.baseDTO import BaseDTO
from django.core.files.uploadedfile import UploadedFile



class GetMediaByIdDTO(BaseDTO):
    media_id: UUID = Field(
        title="Media ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    ),
    is_active: bool = Field(
        default=True, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)


class StorageMediaFilesDTO(BaseDTO):
    files: List[UploadedFile] = Field(
        title="Files", 
        min_length=1,
        examples=["file1.jpg", "file2.jpg", "file3.jpg"],
    ),
    uploader_id: UUID = Field(
        title="Uploader ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )

    @field_validator("files")
    def validate_files(cls, files):
        if not files:
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)

        for f in files:
            if not isinstance(f, UploadedFile):
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)

            if f.size > os.getenv("MAXIMUM_UPLOAD_MB") * 1024 * 1024:
                ExceptionHelper.throw_bad_request(ResponseMessages.FILE_TOO_LARGE)

        return files
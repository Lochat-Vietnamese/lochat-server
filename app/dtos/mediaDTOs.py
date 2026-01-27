import os
from typing import List
from uuid import UUID
from pydantic import Field, field_validator
from app.dtos.baseDTO import BaseDTO
from django.core.files.uploadedfile import UploadedFile



class GetMediaByIdDTO(BaseDTO):
    media_id: UUID = Field(
        title="Media ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )


class StorageMediaFilesDTO(BaseDTO):
    files: List[UploadedFile] = Field(
        title="Files", 
        min_length=1,
        examples=["file1.jpg", "file2.jpg", "file3.jpg"],
    )
    uploader_id: UUID = Field(
        title="Uploader ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )

    @field_validator("files", mode="before")
    def validate_files(cls, files):
        if not files:
            raise ValueError("Missing files")

        for f in files:
            if not isinstance(f, UploadedFile):
                raise ValueError("Invalid file type")

            if f.size > os.getenv("MAXIMUM_UPLOAD_MB") * 1024 * 1024:
                raise ValueError("File too large")

        return files
from uuid import UUID
from pydantic import Field, field_validator
from app.utils.parseBool import ParseBool
from app.dtos.baseDTO import BaseDTO


class GetAllProfileDTO(BaseDTO):
    page: int = Field(
        title="Current Page",
        ge=1,
        default=1, 
        examples=1
    ),
    page_size: int = Field(
        title="Page Size",
        ge=5,
        lt=100,
        default=10, 
        examples=10
    ),
    is_active: bool = Field(
        title="Activity Status",
        default=True, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)

class GetProfileByIdDTO(BaseDTO):
    profile_id: UUID = Field(
        title="Profile ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    ),
    is_active: bool | None = Field(
        title="Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
from datetime import date
from uuid import UUID

from pydantic import Field, field_validator
from app.dtos.baseDTO import BaseDTO
from app.utils.parseBool import ParseBool


class GetMembershipByIdDTO(BaseDTO):
    membership_id: UUID = Field(
        title="Membership ID", 
        example="123e4567-e89b-12d3-a456-426655440000"
    )

class SearchMembershipDTO(BaseDTO):
    profile_id: UUID | None = Field(
        title="Profile ID", 
        example="123e4567-e89b-12d3-a456-426655440000",
        default=None
    )
    conversation_id: UUID = Field(
        title="Conversation ID", 
        example="123e4567-e89b-12d3-a456-426655440000",
        default=None
    )
    last_accessed: date | None = Field(
        title="Last Accessed", 
        example="2023-01-01",
        default=None
    )
    conversation_name: str | None = Field(
        title="Conversation Name", 
        example="Conversation Name",
        default=None
    )
    is_active: bool | None = Field(
        title="Is Active", 
        example=True,
        default=None
    )
    page: int = Field(
        title="Current Page",
        ge=1,
        default=1, 
        examples=1
    )
    page_size: int = Field(
        title="Page Size",
        ge=5,
        lt=100,
        default=10, 
        examples=10
    )

    @classmethod
    def is_only_pagination(cls):
        pagination_fields = {"page", "page_size"}

        for field_name, value in cls.model_dump().items():
            if field_name not in pagination_fields and value is not None:
                return False
        return True
    
    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
    
    @field_validator("last_accessed")
    def validate_last_accessed(cls, input):
        if input is None:
            return input
        if input > date.today():
            raise ValueError("Invalid last accessed date")
        return input